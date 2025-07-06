from django.db import models


class Chat(models.Model):
    user1 = models.ForeignKey(
        to="accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="user1",
    )
    user2 = models.ForeignKey(
        to="accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="user2",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"


class Message(models.Model):
    author = models.ForeignKey(
        to="accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
    )
    text = models.CharField(max_length=256)
    chat = models.ForeignKey(
        to="Chat",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}: {self.text[:30]}"

    class Meta:
        ordering = ["created_at"]
