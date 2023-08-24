from rest_framework import generics, views, status
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

from user.models import User
from user.serializers import (
    UserSerializer,
    UserAuthTokenSerializer,
    ChangePasswordSerializer,
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

    def get_object(self) -> User:
        return self.request.user


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
