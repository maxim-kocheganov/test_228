from pydoc import visiblename
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import enum
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
"""
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        #if not email:
        #    raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
"""
"""
class User(AbstractUser):
      REGISTRED = 1
      AUTOR = 2      
      ROLE_CHOICES = (
          (REGISTRED, 'Registred'),
          (AUTOR, 'Author')
      )
      role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
"""
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    ALL = 'ALL'
    REG = 'REG'
    VISIABILITY = [
        (ALL, 'All'),
        (REG, 'Registred'),
    ]
    visiability = models.CharField(
        max_length=3,
        choices=VISIABILITY,
        default=REG,
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateField()
    content = models.CharField(max_length=2048,blank=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
