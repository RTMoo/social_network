from django.db import models
from django.core.exceptions import ValidationError
from profiles.validators import validate_min_length_if_not_empty


class Profile(models.Model):
    user = models.OneToOneField(to="accounts.CustomUser", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    avatar = models.ImageField(upload_to="profile/avatars/", blank=True, null=True)
    bio = models.TextField(max_length=512, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)

    def clean(self):
        valid, error_message = validate_min_length_if_not_empty(self.first_name)
        if not valid:
            raise ValidationError({"first_name": error_message})

        valid, error_message = validate_min_length_if_not_empty(self.last_name)
        if not valid:
            raise ValidationError({"last_name": error_message})

    def save(self, force_insert=..., force_update=..., using=..., update_fields=...):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)
