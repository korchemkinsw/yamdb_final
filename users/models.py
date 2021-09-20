from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    email = models.EmailField(
        unique=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='о себе',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('id',)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.email
