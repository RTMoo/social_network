from django.db import models


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        to="accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    to_subscribe = models.ForeignKey(
        to="accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="subscribers",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("subscriber", "to_subscribe")
