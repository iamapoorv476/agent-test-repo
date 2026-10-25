import requests

WEBHOOK_URL = "https://hooks.example.com/exports"


def notify_export_ready(email, customer_id):
    try:
        requests.post(WEBHOOK_URL, json={"email": email, "customer_id": customer_id})
    except Exception:
        pass
