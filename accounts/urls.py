from django.urls import path
from .forms import UserLoginForm, PwdResetForm
from .views import SignUpView, ActivateAccountView, PwdResetConfirmView, ResendAccountActivationEmail
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView,  
    PasswordResetCompleteView, 
    PasswordResetDoneView
)

app_name = 'accounts'

urlpatterns = [
    path('login', LoginView.as_view(template_name='account/login.html', form_class=UserLoginForm, redirect_authenticated_user=True), name='login'),
    path('logout', LogoutView.as_view(next_page="accounts:login"), name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('re_activate', ResendAccountActivationEmail.as_view(), name='re_activate_account'),
    path('activate/<uidb64>/<token>', ActivateAccountView.as_view(), name='activate'),
    
    
    path(
        'password/reset_password', 
        PasswordResetView.as_view(
            template_name='account/password/pwd__reset_form.html',
            form_class=PwdResetForm, 
            success_url='pwd_reset_email_sent/',
            email_template_name="account/password/pwd__reset_email.html"
            ), 

        name='password_reset'),

    path(
        'password/pwd_reset_email_sent/',
        PasswordResetDoneView.as_view(
            template_name='account/password/pwd__reset_done.html'
        ),
        name='pwd_email_sent_confirm'
    ),

    path(
        'password/<uidb64>/<token>',
        PwdResetConfirmView.as_view(),
        name='pwd_reset_confirm'
    ),

    path(
        'password/pwd_reset_complete',
        PasswordResetCompleteView.as_view(
            template_name='account/password/pwd__reset_complete.html'
        ),
        name='password_reset_complete'
    )
    
]