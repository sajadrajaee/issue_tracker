from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, PasswordResetForm
from .models import CustomUser
from django import forms
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    model = CustomUser
    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', "first_name", "last_name", "date_joined", 
        )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', 'first_name', 'last_name',
        )
        
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=120, widget=forms.TextInput(
            attrs={'class': 'myfieldclass'}
        )
    )
    password = forms.CharField(
        max_length=150, widget=forms.PasswordInput(
            attrs={'class': 'myfieldclass'}
        )
    )
    
class SetPasswordChangeForm(SetPasswordForm):
    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    class Meta:
        model = CustomUser
        fields = ('email',)