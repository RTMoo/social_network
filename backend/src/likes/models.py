from django.db import models
from django.core.exceptions import ValidationError


class Like(models.Model):
    user = models.ForeignKey(to="accounts.CustomUser", on_delete=models.CASCADE)
    post = models.ForeignKey(
        to="posts.Post", on_delete=models.CASCADE, null=True, blank=True
    )
    comment = models.ForeignKey(
        to="comments.Comment", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ("user", "post"),
            ("user", "comment"),
        )

    def clean(self):
        if (self.post is None) == (self.comment is None):
            raise ValidationError("Лайк должен быть либо на пост, либо на комментарий")
