from email.message import EmailMessage


import aiosmtplib


from app.config import settings

async def send_verification_email(
    recipient_email: str,
    recipient_name: str,
    verification_token: str,
):

    print("===================================")
    print("EMAIL TASK STARTED")
    print("Recipient:", recipient_email)
    print("SMTP Host:", settings.SMTP_HOST)
    print("SMTP Port:", settings.SMTP_PORT)
    print("===================================")


    verification_url = (
    f"{settings.BACKEND_URL}"
    f"/auth/verify-email?token="
    f"{verification_token}"
    )

    message = EmailMessage()

    message["From"] = (
        f"{settings.SMTP_FROM_NAME} "
        f"<{settings.SMTP_FROM_EMAIL}>"
    )

    message["To"] = recipient_email

    message["Subject"] = (
        "Verify your email address"
    )

    message.set_content(
        f"""
Hello {recipient_name},

Thank you for creating an account.

Please verify your email address by clicking
the link below:

{verification_url}

This verification link will expire in
{settings.EMAIL_VERIFICATION_EXPIRE_MINUTES} minutes.

If you did not create this account, you can
safely ignore this email.

Regards,
{settings.SMTP_FROM_NAME}
"""
    )



    print("Connecting to SMTP server...")


    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    )

    print("EMAIL SENT SUCCESSFULLY")
    print("`===================================")



async def send_password_reset_email(
    recipient_email: str,
    full_name: str,
    reset_token: str,
):
    print("===================================")
    print("PASSWORD RESET EMAIL")
    print("Recipient:", recipient_email)
    print("===================================")

    reset_url = (
    f"{settings.FRONTEND_URL}"
    f"/reset-password?token={reset_token}"
)

    message = EmailMessage()

    message["From"] = (
        f"{settings.SMTP_FROM_NAME} "
        f"<{settings.SMTP_FROM_EMAIL}>"
    )

    message["To"] = recipient_email
    message["Subject"] = "Reset Your Password"

    message.set_content(
        f"""
Hello {full_name},

We received a request to reset your password.

Click the link below to reset your password:

{reset_url}

This link will expire in
{settings.PASSWORD_RESET_EXPIRE_MINUTES} minutes.

If you did not request a password reset,
you can safely ignore this email.

Regards,
{settings.SMTP_FROM_NAME}
"""
    )

    print("Connecting to SMTP server...")

    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    )

    print("PASSWORD RESET EMAIL SENT SUCCESSFULLY")
    print("===================================")