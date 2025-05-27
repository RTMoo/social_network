from django.db import models
from profiles.validators import validate_min_length_if_not_empty


class Profile(models.Model):
    user = models.OneToOneField(to="accounts.CustomUser", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, blank=True, default="")
    last_name = models.CharField(max_length=32, blank=True, default="")
    avatar = models.ImageField(upload_to="profile/avatars/", blank=True, null=True)
    bio = models.TextField(max_length=512, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)

    def clean(self):
        validate_min_length_if_not_empty(
            field_name="first_name", value=self.first_name, is_model_exception=True
        )

        validate_min_length_if_not_empty(
            field_name="last_name", value=self.last_name, is_model_exception=True
        )

    def save(self, force_insert=..., force_update=..., using=..., update_fields=...):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)
