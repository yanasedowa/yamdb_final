from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime


def current_year():
    return datetime.date.today().year


class User(AbstractUser):
    username = models.TextField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.TextField(max_length=150, blank=True)
    last_name = models.TextField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=50, default='1')

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    USER_ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    role = models.CharField(
        max_length=max(len(role[0]) for role in USER_ROLES),
        choices=USER_ROLES,
        default=USER
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
