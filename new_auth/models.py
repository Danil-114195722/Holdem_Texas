from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


DEFAULT_PROFILE_PHOTO = 'profile_photo/default_user_profile_photo.png'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email'),
        max_length=150,
        unique=True,
        null=False,
        blank=False
    )
    date_added = models.DateTimeField(
        verbose_name=_('date added'),
        auto_now_add=True,
        null=False,
        blank=False
    )
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
        null=False,
        blank=False
    )
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=True,
        help_text=_("Should user be treated as active? Unselect this instead of deleting accounts."),
        null=False,
        blank=False
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
