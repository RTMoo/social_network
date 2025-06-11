from django.db import models


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(
        to="accounts.CustomUser",
        related_name="sent_requests",
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        to="accounts.CustomUser",
        related_name="received_requests",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")


class Friendship(models.Model):
    user1 = models.ForeignKey(
        to="accounts.CustomUser",
        related_name="friendships1",
        on_delete=models.CASCADE,
    )
    user2 = models.ForeignKey(
        to="accounts.CustomUser",
        related_name="friendships2",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")
