from django.db import models
from django.core.validators import MinLengthValidator


class Profile(models.Model):
    user = models.OneToOneField(to="accounts.CustomUser", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, validators=[MinLengthValidator(2)])
    last_name = models.CharField(max_length=32, validators=[MinLengthValidator(2)])
    avatar = models.ImageField(upload_to="profile/avatars/")
    bio = models.TextField(max_length=512, blank=True, null=True)
    birth_date = models.DateField()
    country = models.CharField(max_length=2)  # библиотека django-countries
