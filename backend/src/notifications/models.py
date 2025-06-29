from django.db import models


class Notification(models.Model):
    class Types(models.TextChoices):
        NEW_POST = "new_post", "Новый пост"
        LIKE = "like", "Лайк"
        COMMENT = "comment", "Комментарий"

    to_user = models.ForeignKey(
        to="accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="received_notifications",
    )
    from_user = models.ForeignKey(
        to="accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_notifications",
    )
    type = models.CharField(
        max_length=32,
        choices=Types.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
