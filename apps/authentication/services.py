from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from apps.users.models import User
from apps.authentication.emails import send_password_reset_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str

class AuthenticationService:
    @staticmethod
    def generate_reset_link(user):
        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )
        token = PasswordResetTokenGenerator().make_token(user)
        reset_link = (
            f"{settings.FRONTEND_URL}"
            f"/reset-password"
            f"?uid={uid}"
            f"&token={token}"
        )

        return {
            "uid": uid,
            "token": token,
            "reset_link": reset_link,
        }


    @staticmethod
    def forgot_password(email):
        try:
            user = User.objects.get(
                email=email
            )
        except User.DoesNotExist:
            return

        data = AuthenticationService.generate_reset_link(
            user
        )

        send_password_reset_email(
            user=user,
            reset_link=data["reset_link"]
        )


    @staticmethod
    def reset_password(uid, token, password):
        try:
            user_id = force_str(
                urlsafe_base64_decode(uid)
            )

            user = User.objects.get(
                pk=user_id
            )

        except Exception:
            return False

        if not PasswordResetTokenGenerator().check_token(
                user,
                token
        ):
            return False

        user.set_password(password)
        user.save()

        return True