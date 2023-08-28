from user.models import Follow


def get_follow_object(follower_id: int, user_id: int) -> Follow | None:
    follow = Follow.objects.filter(follower_id=follower_id).filter(
        user_id=user_id
    )
    if follow.exists():
        return follow
    return None
