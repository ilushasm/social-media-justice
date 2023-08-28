from post.models import Like


def get_like_object(post_id: int, user_id: int) -> Like | None:
    like = Like.objects.filter(post_id=post_id).filter(created_by_id=user_id)
    if like.exists():
        return like
    return None


def get_author(instance) -> str:
    if (
        instance.created_by.first_name is not None
        and instance.created_by.last_name is not None
    ):
        return (
            f"{instance.created_by.first_name} "
            f"{instance.created_by.last_name} "
            f"(@{instance.created_by.username})"
        )
    return f"@{instance.created_by.username}"
