import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class UserRoles(models.TextChoices):
        superadmin = 'sa', 'superadmin'
        admin = 'a', 'admin'
        teacher = 't', 'teacher'
        student = 's', 'student'

    avatar = models.ImageField(upload_to="avatar/",
                               validators=[FileExtensionValidator(["jpg", "jpeg", "png", "heic", "heif", "svg", "webp"])],
                               null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=13, unique=True)
    role = models.CharField(max_length=2, choices=UserRoles.choices, default=UserRoles.student)
    password = models.CharField(max_length=123)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'


    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
