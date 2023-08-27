from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import (
    CreateUserView,
    ProfileUserView,
    LogoutView,
    LogoutAllView,
    ChangePasswordView,
    FollowUserView,
    UnfollowUserView,
    SearchUserView,
    ListOfFollowersView,
    ListOfFollowingView,
)

urlpatterns = [
    path(
        "register/",
        CreateUserView.as_view(),
        name="register",
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", LogoutView.as_view(), name="token_logout"),
    path("logout_all/", LogoutAllView.as_view(), name="auth_logout_all"),
    path("change_password/", ChangePasswordView.as_view(), name="change-password"),
    path("profile/", ProfileUserView.as_view(), name="my-profile"),
    path("profile/<int:user_id>/", ProfileUserView.as_view(), name="user-profile"),
    path("profile/<int:user_id>/follow/", FollowUserView.as_view(), name="follow"),
    path(
        "profile/<int:user_id>/unfollow/", UnfollowUserView.as_view(), name="unfollow"
    ),
    path(
        "profile/<int:user_id>/followers_list/",
        ListOfFollowersView.as_view(),
        name="list-of-followers",
    ),
    path(
        "profile/<int:user_id>/following_list/",
        ListOfFollowingView.as_view(),
        name="following-list",
    ),
    path("search/", SearchUserView.as_view(), name="user-search"),
]

app_name = "user"
