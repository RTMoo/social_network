from posts.models import Post


def get_user_posts(username: str):
    posts = (
        Post.objects.filter(author__username=username).select_related("author").all()
    )

    return posts
