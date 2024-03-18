from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.contrib.auth.models import Group, Permission

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class UserManagement(AbstractUser):
    email = models.EmailField(unique=True)
    verification_code = models.CharField(max_length=100)
    objects = CustomUserManager()
    groups = models.ManyToManyField(
        Group,
        related_name="user_management_set",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_management_set",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.username is None or self.username == "":
            self.username = self.email
        super().save(*args, **kwargs)
