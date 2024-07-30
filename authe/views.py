from django.shortcuts import render
from .models import CustomUser
from django.http import Http404
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, SetPasswordChangeForm, PasswordResetForm, LoginForm
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
#for getting the domain name of current site, this is often used for generating
#unique tokens.
from django.contrib.sites.shortcuts import get_current_site
#it encodes a str(pk of user) into a url-safe base64 str.
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#it converts a str or obj to a byte str in django, it is used with combination
#with other functions like encoding or hashing functions
from django.utils.encoding import force_bytes
#is a django activation code generator, it is used for generating token for
#user's account activation of password reset in code
from django.contrib.auth.tokens import default_token_generator
#used for sending emails, provides functionaliteis like, subject, recipent, body and ...
from django.core.mail import EmailMessage

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        
            user = authenticate(
                request,
                username=username,
                password = password
            )
            #checks for any password or username problem
            if user is not None:
                login(request, user)
                return redirect('projects:homepage')
            else:
                messages.error(request, "invalid username or password")
                return redirect('authe:login')
    else:
        form = LoginForm()    
    return render(request, 'authe/login.html', {'form':LoginForm})
    
def registerpage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
        
            if CustomUser.objects.filter(username=username).exists():
            # render a message and redirect to register page
                messages.info(request, "User with this username already exist")
                return redirect('register')
            #if user did not exist, then redirect to register page to create account
        
            user = CustomUser.objects.create_user(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
        
            user.set_password(password)
            user.save()
            subject = 'user creation account'
            message = f'{user.username} you have successfully created account'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(
                subject,
                message,
                email_from,
                recipient_list
            ) #question : how to set send email like if email was not sent successfully we recive an email in application that the email was not send?
            messages.success(request, "account created successfully!")
            return redirect('authe:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authe/register.html', {'form':form})

def log_out(request):
    logout(request)
    #where does the following message must be displayed and how to do that?
    messages.success(request, "successfully logged out!")
    return redirect('authe:login')

@login_required(login_url='authe:login')
def profile(request):
    # items = CustomUser.objects.all()
    return render(request, 'authe/profile.html', {})

@login_required(login_url="authe:login")
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            
            form.save()
            messages.success(request,"you have successfully edited your profile.")
            return redirect('authe:profile')
        
    else:
        form = CustomUserChangeForm(instance = request.user)
    
    return render(request, 'authe/editprofile.html', {'form':form})

@login_required(login_url='authe:login') #user must be logined to change the password 
def change_password(request):
    if request.method == 'POST':
        form = SetPasswordChangeForm(request.user, request.POST) 
        #if user is not logged in then request.user points to an anonymousUser(virtual user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "password changed succuessfully!")
            return redirect('projects:homepage')
        form.add_error(request, "password change process faild! try again")
    else:
        form = SetPasswordChangeForm(request.user)
    return render(request, 'authe/change_password.html', {'form':form})


def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)        
        if form.is_valid():
            email = form.cleaned_data['email']
            UserModel = CustomUser
            try:
                user = UserModel.objects.get(email=email) # it is why email must be unique. 
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                # Constructing the password reset URL
                current_site = get_current_site(request)
                reset_url = f"{current_site}/password_reset/{uid}/{token}/"

                # Send the password reset email to the user
                message = render_to_string('authe/password_reset_email.html', { #the template(1st item)
                    'user': user, #this is the context for render_to_str func
                    'reset_url': reset_url,
                })
                mail_subject = f'email varification! '
                email = EmailMessage(mail_subject, message, to=[email]) #subject, body, to
                email.send()

                return redirect('authe:password_reset_done')
            except UserModel.DoesNotExist:
                # Handle the case where the user does not exist
                raise Http404("user with that email does not exist!!")
            
    else:
        form = PasswordResetForm()
    return render(request, 'authe/password_reset_request.html', {'form': form})

def password_reset_confirm(request, uidb64, token):  #this is when user click on reset url
    try:
        uid = urlsafe_base64_decode(uidb64).decode() #uid was encoded in 1st step, it is going to be decoded now
        user = CustomUser.objects.get(pk=uid) 
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST) 
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "password changed succuessfully!")
                return redirect('projects:homepage')
            form.add_error(request, "password change process faild! try again")
        else:
            form = SetPasswordForm(None)
        return render(
            request, 'authe/password_reset_confirm.html', {'form':form}
        )
        
    return render(request, 'authe/password_reset_confirm.html', {})

#3rd step, after reset email sent to user will be rendered to tell
#user to check his/her email box.
def password_reset_done(request):
    
    return render(
        request, 'authe/password_reset_done.html', {}
    )

def password_reset_complete(request):
    return render(request, 'authe/password_reset_complete.html', {})

def password_reset_email(request):
    return render(request, 'authe/password_reset_email.html', {})