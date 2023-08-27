from typing import Type, Tuple, Optional

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics, views, status
from rest_framework.serializers import Serializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    OutstandingToken,
    BlacklistedToken,
)

from user.models import Follow
from user.serializers import (
    UserSerializer,
    UserAuthTokenSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    FollowerSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = UserAuthTokenSerializer


class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request) -> Response:
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(views.APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request) -> Response:
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class ProfileUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> get_user_model():
        if "user_id" in self.kwargs:
            user_id = self.kwargs["user_id"]
            return get_object_or_404(get_user_model().objects.all(), pk=user_id)
        return self.request.user

    def get_serializer_class(self) -> Type[Serializer]:
        if self.get_object() == self.request.user:
            return UserSerializer
        return UserProfileSerializer


class ChangePasswordView(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            if not user.check_password(old_password):
                return Response(
                    {"old_password": ["Incorrect password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"message": "Password successfully changed."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_follow_info(
    request, user_id: int = None
) -> Tuple[Optional[get_user_model()], Optional[get_user_model()]]:
    if user_id is not None and user_id > 0:
        follower = request.user
        followed = get_user_model().objects.filter(id=user_id)[0]

        return follower, followed

    return None, None


class FollowUserView(views.APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, user_id: int) -> Response:
        follower, followed = get_follow_info(request, user_id)

        if followed:
            if not Follow.objects.filter(follower=follower, user=followed).exists():
                Follow.objects.create(follower=follower, user=followed)
                return Response(
                    {"message": f"You are now following {followed.first_name}"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"message": f"You are already following {followed.first_name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "User not found or data is invalid"},
            status=status.HTTP_404_NOT_FOUND,
        )


class UnfollowUserView(views.APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def delete(request, user_id: int) -> Response:
        follower, followed = get_follow_info(request, user_id)

        if followed:
            user_follow = Follow.objects.filter(
                follower=follower, user=followed
            ).first()
            if user_follow:
                user_follow.delete()
                return Response(
                    {"message": f"You have unfollowed {followed.first_name}"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": f"You are not following {followed.first_name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "User not found or data is invalid"},
            status=status.HTTP_404_NOT_FOUND,
        )
