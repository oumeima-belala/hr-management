from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, LogoutSerializer, LoginResponseSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers import UserProfileSerializer
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from .services import AuthenticationService
from .swagger import (
    login_schema,
    me_schema,
    logout_schema,
    forgot_password_schema,
    reset_password_schema,
)

@login_schema
class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = data["user"]

        return Response(
            {
                "access": data["access"],

                "refresh": data["refresh"],

                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                }
            },
            status=status.HTTP_200_OK
        )

@me_schema
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserProfileSerializer(
            request.user,
            context={"request": request}
        )

        return Response(serializer.data)


@logout_schema
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Logout successful."
            },
            status=status.HTTP_200_OK
        )

@forgot_password_schema
class ForgotPasswordView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ForgotPasswordSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        AuthenticationService.forgot_password(
            serializer.validated_data["email"]
        )

        return Response(
            {
                "message": (
                    "If an account exists with this email, "
                    "a password reset link has been sent."
                )
            },
            status=status.HTTP_200_OK
        )

@reset_password_schema
class ResetPasswordView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        success = AuthenticationService.reset_password(

            uid=serializer.validated_data["uid"],

            token=serializer.validated_data["token"],

            password=serializer.validated_data["password"],
        )

        if not success:

            return Response(
                {
                    "message":
                    "Le lien de réinitialisation est invalide ou expiré."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message":
                "Mot de passe réinitialisé avec succès."
            },
            status=status.HTTP_200_OK
        )