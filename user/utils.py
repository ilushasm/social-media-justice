from typing import Tuple, Optional

from django.contrib.auth import get_user_model

from user.models import Follow


def get_followers_or_following(user_id, filter_followers=True) -> list[int]:
    field_name = "user_id" if filter_followers else "follower_id"
    related_field_name = "follower" if filter_followers else "user"

    follows = Follow.objects.filter(**{field_name: user_id}).select_related(
        related_field_name
    )
    users_id = [
        item.follower_id if filter_followers else item.user_id for item in follows
    ]

    return users_id


def get_follow_info(
    request, user_id: int = None
) -> Tuple[Optional[get_user_model()], Optional[get_user_model()]]:
    if user_id is not None and user_id > 0:
        follower = request.user
        followed = get_user_model().objects.filter(id=user_id)[0]

        return follower, followed

    return None, None
