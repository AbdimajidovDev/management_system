import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
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


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Users must have a valid phone number')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.UserRoles.superadmin)
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class UserRoles(models.TextChoices):
        superadmin = 's', 'Super Admin'
        admin = 'a', 'Admin'
        teacher = 't', 'Teacher'

    avatar = models.ImageField(upload_to="avatar/",
                               validators=[FileExtensionValidator(["jpg", "jpeg", "png", "heic", "heif", "svg", "webp"])],
                               null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=13, unique=True)
    role = models.CharField(max_length=2, choices=UserRoles.choices, default=UserRoles.teacher)
    password = models.CharField(max_length=123)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    def __str__(self):
        return f"{self.role} - {self.full_name}"

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
