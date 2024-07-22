import logging

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app.api.app_auth.serializers import AuthSerializer, UserSerializer

logger = logging.getLogger(__name__)
User = get_user_model()


class LoginView(APIView):
    """ """

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        """
        Endpoint to authenticate a user
        """
        serializer = AuthSerializer(request.data)
        serializer.is_valid(raise_exception=True)

        # Perform authentication
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # call the django authenticate method
        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh_token = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "User logged in successfully",
                    "access": str(refresh_token.access_token),
                    "refresh": str(refresh_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "error": "Invalid credentials",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        """
        Endpoint to register a user account
        """
        serializer = UserSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # perform token generation and render it in API
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": serializer.data,
                "message": "User account successfully created",
                "refresh": str(refresh.token),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
