from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


# Create a manager tto dictate how objects will be created

class CustomUserManager(BaseUserManager):
    # overide user_create method
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Please set a valid email. Email')
        email=self.normalize_email(email)
        email = email.lower()
        new_user = self.model(email=email, **extra_fields)
        
        new_user.set_password(password)
        new_user.save()
        
        return new_user
    
    def create_superuser(self, email, password, **extra_fields):
        # set default values for superadmin
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)
    
    
class AuthUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = PhoneNumberField(unique=True, blank=False, null=False)
    
    REQUIRED_FIELDS=['username']
    USERNAME_FIELD='email'
    
    def __str__(self):
        return self.username

