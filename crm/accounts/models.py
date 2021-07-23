from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

import django.utils.timezone as timezone
from .utils import ROLES


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model 
    """
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=100, choices=ROLES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
