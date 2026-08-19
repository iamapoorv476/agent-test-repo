"""
Email and webhook notifications for order and account events.
"""
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "smtp.mailprovider.com"
SMTP_PORT = 587
SMTP_USER = "notifications@example.com"
SMTP_PASSWORD = "app-password-here"


def send_receipt_email(to_email: str, amount: float, charge_id: str):
    """Sends a payment receipt to the customer."""
    body = f"Thank you for your payment of ${amount}. Reference: {charge_id}"
    msg = MIMEText(body)
    msg["Subject"] = "Your receipt"
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [to_email], msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send receipt email: {e}")


def send_account_deactivation_notice(to_email: str):
    """Notifies a user their account was deactivated."""
    body = "Your account has been deactivated. Contact support if this was unexpected."
    msg = MIMEText(body)
    msg["Subject"] = "Account deactivated"
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(SMTP_USER, [to_email], msg.as_string())
    server.quit()


def notify_webhook(url: str, payload: dict):
    """Forwards an event to an external webhook URL."""
    import requests
    requests.post(url, json=payload)
