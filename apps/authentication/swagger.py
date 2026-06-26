from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

from .serializers import (
    LoginSerializer,
    LoginResponseSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    LogoutSerializer,
)

from apps.users.serializers import UserProfileSerializer

login_schema = extend_schema(

    tags=["Authentication"],

    summary="User Login",

    description="""
Authenticate a user using email and password.

Returns:

- JWT Access Token
- JWT Refresh Token
- User information
""",

    request=LoginSerializer,

    responses={
        200: LoginResponseSerializer,

        400: OpenApiResponse(
            description="Invalid email or password."
        ),
    },

    examples=[

        OpenApiExample(

            "Login",

            summary="Login Example",

            value={
                "email": "admin@company.com",
                "password": "Password123!"
            },

            request_only=True,
        ),

        OpenApiExample(

            "Success",

            summary="Successful Login",

            value={

                "access": "...",

                "refresh": "...",

                "user": {

                    "id": 1,

                    "email": "admin@company.com",

                    "role": "ADMIN",

                    "is_active": True,

                    "employee": {

                        "id": 1,

                        "first_name": "John",

                        "last_name": "Doe"

                    }

                }

            },

            response_only=True,

            status_codes=["200"]

        )

    ]

)

me_schema = extend_schema(

    tags=["Authentication"],

    summary="Current User",

    description="""
Return the authenticated user's profile.
""",

    responses={
        200: UserProfileSerializer
    }

)

logout_schema = extend_schema(

    tags=["Authentication"],

    summary="Logout",

    description="""
Blacklist the refresh token and logout the current user.
""",

    request=LogoutSerializer,

    responses={

        200: OpenApiResponse(
            description="Logout successful."
        )

    }

)


forgot_password_schema = extend_schema(

    tags=["Authentication"],

    summary="Forgot Password",

    description="""
Send a password reset email if the account exists.
""",

    request=ForgotPasswordSerializer,

    responses={

        200: OpenApiResponse(
            description="Email sent if account exists."
        )

    }

)


reset_password_schema = extend_schema(

    tags=["Authentication"],

    summary="Reset Password",

    description="""
Reset the user's password using uid and token.
""",

    request=ResetPasswordSerializer,

    responses={

        200: OpenApiResponse(
            description="Password successfully reset."
        ),

        400: OpenApiResponse(
            description="Invalid token."
        )

    }

)