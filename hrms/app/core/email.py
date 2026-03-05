import smtplib
from email.mime.text import MIMEText
from app.core.config import settings


def send_email(to_email: str, subject: str, body: str):

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.send_message(msg)