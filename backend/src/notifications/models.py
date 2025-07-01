from django.db import models
from django.db.models import Q


class Notification(models.Model):
    class Types(models.TextChoices):
        NEW_POST = "new_post", "Новый пост"
        LIKE = "like", "Лайк"
        COMMENT = "comment", "Комментарий"
        SUBSCRIBE = "subscribe", "Подписка"

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
    post = models.ForeignKey(
        to="posts.Post",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    comment = models.ForeignKey(
        to="comments.Comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["from_user", "to_user", "type", "post"],
                condition=Q(type="like"),
                name="unique_like_notification",
            ),
            models.UniqueConstraint(
                fields=["from_user", "to_user", "type"],
                condition=Q(type="subscribe"),
                name="unique_subscribe_notification",
            ),
        ]
        ordering = ["-created_at"]
