from likes.models import Like


def get_user_likes_by_type(username: str, type: str):
    """
    Возвращает все лайки, поставленные пользователем с указанным именем к комментариям или постам.

    Args:
        username: str - имя пользователя

    Returns:
        Queryset[Like | Comment]
    """

    if type == "post":
        likes = Like.objects.filter(user__username=username, post__isnull=False).select_related("post__author").all()
        posts = [like.post for like in likes]
        
        return posts
    elif type == "comment":
        likes = Like.objects.filter(user__username=username, comment__isnull=False).select_related("comment__author").all()
        comments = [like.comment for like in likes]

        return comments

    raise ValueError("Invalid type")
