from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return "images_user_perfil/{0}_{1}".format(instance.id, filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("First Name"), max_length=120, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=120, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    image = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    birthday = models.DateField(null=True, blank=True)
    curp = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)

    recovery_code = models.CharField(max_length=6, null=True, blank=True, default=None)
    recovery_code_email = models.EmailField(blank=True, null=True)
    remaining_attempts = models.SmallIntegerField(null=True, blank=True, default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def nombre_completo(self):
        return "{}{}".format(
            self.first_name if self.first_name else "",
            " " + self.last_name if self.last_name else "",
        )

    def __str__(self):
        return self.email
