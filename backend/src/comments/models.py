from django.db import models


class Comment(models.Model):
    post = models.ForeignKey(
        to="posts.Post",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        to="accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="comments",
    )
    thread = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="thread_comments",
    )
    reply_to = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="replies_to",
    )
    reply_to_author = models.ForeignKey(
        to="accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="reply_to_comments",
    )
    text = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
