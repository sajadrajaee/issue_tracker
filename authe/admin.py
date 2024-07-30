from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    #fieldsets is used to style and manage items defined in userchange form
    fieldsets = (  
        (
            "User Info", {"fields" : ( "username", "first_name", "last_name", "email", "password")}  
        ),
        (
            "permission", {"fields":("is_active", "is_staff", "groups", "user_permissions")}
        )
    ) 
    #this is used to display items that are going to create a new instance of model (creating new user)
    add_fieldsets = (
        (None, {
            "classes" : ("wide",), #this is css class for styling registration form on admin panel of django
            "fields" :(
                "date_joined",
                "username",
                "first_name",
                "last_name",
                "email",
                "password1",
                "password2",
                "groups",
                "user_permissions"
                )
            }
        ),
    )
    list_display = (
        "username",
        "email",
        "date_joined",
        "is_active",
        "is_staff"
    )
    list_filter = ("date_joined",)
    ordering = ("email",)
    search_fields = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)
