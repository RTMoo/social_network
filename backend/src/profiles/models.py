from django.db import models
from django.core.validators import MinLengthValidator


class Profile(models.Model):
    user = models.OneToOneField(to="accounts.CustomUser", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, validators=[MinLengthValidator(2)], blank=True, null=True)
    last_name = models.CharField(max_length=32, validators=[MinLengthValidator(2)], blank=True, null=True)
    avatar = models.ImageField(upload_to="profile/avatars/", blank=True, null=True)
    bio = models.TextField(max_length=512, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)  # библиотека django-countries
