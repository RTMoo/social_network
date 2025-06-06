from posts.models import Post
from comments.models import Comment


def change_likes_count(obj: Post | Comment, increment: bool = True):
    if increment:
        obj.likes_count += 1
    else:
        obj.likes_count -= 1

    obj.save()
