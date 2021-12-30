from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail

class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        if password is None:
            raise ValueError('Password should not be none')

        return self.create_user(username=username, email=email,  password=password, **kwargs)
        

    def create_user(self, username, email, password=None, **kwargs):
        if email is None:
            raise ValueError('You must provide an email address')
        if username is None:
            raise ValueError('Users should have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

def handle_profile_upload(instance, filename):
    return f"profile_img//myimage_{instance.pk}/{filename}"

class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    profile_pic = models.ImageField(upload_to=handle_profile_upload, default='profile_img/no_image.jpg')
    biography = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'hearme@easy.com',
            [self.email],
            fail_silently=False,
        )

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email
