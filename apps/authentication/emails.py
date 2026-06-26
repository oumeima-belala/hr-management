from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_test_email(to_email):

    send_mail(
        subject="Test Email",
        message="Congratulations! Your Django email configuration works correctly.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
    )

def send_password_reset_email(user, reset_link):

    subject = "Password Reset Request"

    full_name = (
        f"{user.employee.first_name} "
        f"{user.employee.last_name}"
    )

    html_content = render_to_string(
        "emails/reset_password.html",
        {
            "full_name": full_name,
            "reset_link": reset_link,
        }
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body="Password Reset",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.attach_alternative(
        html_content,
        "text/html"
    )

    email.send()