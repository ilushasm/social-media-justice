from post.models import Like


def get_like_object(post_id: int, user_id: int) -> Like | None:
    like = Like.objects.filter(post_id=post_id).filter(created_by_id=user_id)
    if like.exists():
        return like
    return None
