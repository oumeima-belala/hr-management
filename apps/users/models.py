from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from .managers import UserManager

class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Administrator"
    HR = "HR", "Human Resources"
    ACCOUNTANT = "ACCOUNTANT", "Accountant"
    WORKSHOP_MANAGER = "WORKSHOP_MANAGER", "Workshop Manager"
    ASSISTANT = "ASSISTANT", "Assistant"

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.ASSISTANT
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["email"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_hr(self):
        return self.role == UserRole.HR

    def __str__(self):
        return self.email