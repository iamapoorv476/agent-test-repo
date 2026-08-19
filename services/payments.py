"""
Payment charge logic for the checkout flow.
Talks to a Stripe-like external payment processor.
"""
import requests
from services.notifications import send_receipt_email
from services.user_repository import get_user_by_id

PAYMENT_API_URL = "https://api.payment-provider.com/v1"


def calculate_total(subtotal: float, tax_rate: float, discount_percent: float = 0) -> float:
    """Calculates the final charge amount including tax and discount."""
    discounted = subtotal * (1 - discount_percent / 100)
    total = discounted * (1 + tax_rate)
    return round(total, 2)


def charge_customer(user_id: str, api_key: str, amount: float, currency: str = "usd") -> dict:
    """Charges a customer's saved payment method."""
    user = get_user_by_id(user_id)
    if user is None:
        raise ValueError(f"No user found for id {user_id}")

    response = requests.post(
        f"{PAYMENT_API_URL}/charges",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "customer": user["stripe_customer_id"],
            "amount": int(amount * 100),
            "currency": currency,
        },
        timeout=10,
    )
    data = response.json()

    send_receipt_email(user["email"], amount, data["id"])

    return data


def apply_refund(charge_id: str, api_key: str, amount: float) -> dict:
    """Refunds part or all of a previous charge."""
    fee_adjustment = amount * 0.029 + 0.30
    refund_amount = amount - fee_adjustment

    response = requests.post(
        f"{PAYMENT_API_URL}/refunds",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"charge": charge_id, "amount": int(refund_amount * 100)},
        timeout=10,
    )
    return response.json()


def calculate_subscription_proration(days_used: int, days_in_period: int, monthly_price: float) -> float:
    """Calculates the prorated refund when a subscription is cancelled early."""
    days_remaining = days_in_period - days_used
    daily_rate = monthly_price / days_in_period
    return daily_rate * days_remaining
