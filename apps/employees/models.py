from django.db import models
from django.conf import settings
from datetime import date

class Gender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"

class FamilyStatus(models.TextChoices):
    SINGLE = "SINGLE", "Single"
    MARRIED = "MARRIED", "Married"
    DIVORCED = "DIVORCED", "Divorced"
    WIDOWED = "WIDOWED", "Widowed"

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    social_security_number = models.CharField(
        max_length=30,
        unique=True
    )
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices
    )
    family_status = models.CharField(
        max_length=20,
        choices=FamilyStatus.choices
    )
    birth_date = models.DateField()
    photo = models.ImageField(
        upload_to="employees/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        today = date.today()

        return (
                today.year
                - self.birth_date.year
                - (
                        (today.month, today.day)
                        <
                        (self.birth_date.month, self.birth_date.day)
                )
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

