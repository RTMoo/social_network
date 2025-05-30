from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        to="accounts.CustomUser", on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=128)
    content = models.TextField(max_length=2000)
    image = models.ImageField(upload_to="posts/post_images/", blank=True, null=True)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.author.username}"
