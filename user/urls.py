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
)

urlpatterns = [
    path(
        "register/",
        CreateUserView.as_view(),
        name="register",
    ),
    path("profile/", ProfileUserView.as_view(), name="profile"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", LogoutView.as_view(), name="token_logout"),
    path("logout_all/", LogoutAllView.as_view(), name="auth_logout_all"),
    path("change_password/", ChangePasswordView.as_view(), name="change-password"),
]

app_name = "user"
