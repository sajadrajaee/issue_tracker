from django.urls import path
from .views import *

app_name = 'authe'
urlpatterns = [
    path('login/', login_page, name="login"),
    path('register/', registerpage, name="register"),
    path('logout/', log_out, name="logout"),
    path('profile/', profile, name="profile"),
    path('editprofile/', edit_profile, name="edit_profile"),
    
    #password management
    path('password_change/', change_password, name="change_password"), #done
    path('password_reset/', password_reset_view, name="password_reset_request"),#user request to reset password(first step)
    path('password_reset/done/', password_reset_done, name="password_reset_done"),
    path('password_reset/<uidb64>/<token>/', password_reset_confirm, name="password_reset_confirm"), #second step
    path('reset_password/done/', password_reset_complete, name="password_reset_complete")
]
