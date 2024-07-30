import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dataclasses import dataclass

from config import (
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
)


@dataclass
class SMTPConfig:
    smtp_server: str
    smtp_port: int
    username: str
    password: str


def get_smtp_config():
    return SMTPConfig(
        smtp_server=EMAIL_HOST,
        smtp_port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
    )


def send_email(
    subject: str,
    message: str,
    from_email: str,
    recipient_list: list[str],
    smtp_config: SMTPConfig,
):
    """
    Send an email using smtplib and email libraries.
    """
    smtp_server = smtp_config.smtp_server
    smtp_port = smtp_config.smtp_port
    username = smtp_config.username
    password = smtp_config.password
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = ", ".join(recipient_list)
        msg["Subject"] = subject

        # Attach the email body
        msg.attach(MIMEText(message, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(username, password)
            server.sendmail(from_email, recipient_list, msg.as_string())

        print(f"Email sent successfully to {', '.join(recipient_list)}")
    except Exception as e:
        print(f"Failed to send email: {e}")
