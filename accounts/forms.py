from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

User = get_user_model()

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(error_messages={'required': 'Sorry, please enter your username'}, widget=forms.EmailInput(
        attrs={'id': 'login__username',
        'placeholder': 'Username'}))
    password = forms.CharField(error_messages={'required': 'Sorry, please enter your password'}, widget=forms.PasswordInput(
        attrs={
            
            'id': 'login__password',
            'placeholder': 'Password'
        }
    ))

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.get(email=username)
        
        if user is None:
            raise forms.ValidationError('This username doesn\'t exist, please provide a valid username')

        return username

class RegistrationForm(forms.ModelForm):
    """
    Registration Form - create new user using username, email and password
    """

    error_messages = {
        'password_mismatch': 'Passwords doesn\'t match',
        'username_exists': 'This username already exists, please choose another username',
        'email_exists': 'This email already exists, please choose another email'
    }


    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'form_username'}))
    email = forms.EmailField(max_length=100,  error_messages={'required': 'Sorry, please enter your email'}, widget=forms.EmailInput(
        attrs={'id': 'form_email'}))
    phone = forms.CharField(max_length=15,  error_messages={'required': 'Sorry, please enter your cellphone number'} ,widget=forms.TextInput(attrs={'id': 'form_phone'}))
    password = forms.CharField(error_messages={'required': 'Sorry, please enter your password'}, widget=forms.PasswordInput(attrs={'id': 'form_password'}), strip=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'form_password2'}), strip=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'password2']

    def clean_username(self):
        
        """
        Check if the username already exists
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['username_exists'])
        return username

    def clean_email(self):

        """
        Checks if the email already exists
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages['email_exists'])

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class AccountActivationForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'id': 'activate_form_email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.get(email=email)

        if not user:
            raise forms.ValidationError(
                'Email doesn\'t exists')
        if user.is_active:
            raise forms.ValidationError('Account already verified')
        return email

class PwdResetForm(PasswordResetForm):
    """
    Custom password reset form
    """

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'id': 'reset_form_email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Unfortunatley we can not find this email address')
        if not User.objects.get(email=email).is_active:
            raise forms.ValidationError('Unfortunatley, your email address is not verified')

        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
            attrs={'placeholder': 'New password', 'id': 'reset_form_newpassword'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
            attrs={'placeholder': 'Retype-New password', 'id': 'reset_form_newpassword2'}))

class UpdateForm(forms.ModelForm):

    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'form_username', 'readonly': 'readonly'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'id': 'form_email', 'readonly': 'readonly'}))
    first_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'First name', 'id':'form_firstname'}))
    last_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Last name', 'id': 'form_lastname'}))
    profile_pic = forms.ImageField()
    biography = forms.Textarea()


        
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_pic', 'biography']

