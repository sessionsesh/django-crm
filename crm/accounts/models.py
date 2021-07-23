from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

import django.utils.timezone as timezone
from accounts.utils import ROLECHOICES


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model 
    """
<<<<<<< HEAD
    username = models.CharField(max_length=30, blank=True)
=======
    username = models.CharField(max_length=80, unique=True, blank=True)
>>>>>>> a101da8c1ed381fc58fc9eed789a1d63412e45e4
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=100, choices=ROLECHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
