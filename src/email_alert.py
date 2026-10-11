
import os
import re
import json
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = "output"
HISTORY_FILE = os.path.join(OUTPUT_DIR, "alert_history.json")


def convert_price(value):
    """Convert a price such as '3,875' into a number."""
    if value is None:
        return None

    try:
        cleaned = re.sub(
            r"[^\d.]",
            "",
            str(value).replace(",", "")
        )
        return float(cleaned) if cleaned else None
    except (ValueError, TypeError):
        return None


def load_alert_history():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(HISTORY_FILE):
        return {}

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read alert history.")
        return {}


def save_alert_history(history):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def send_price_alert(product):
    """Send a price alert email."""
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if not all([sender_email, sender_password, receiver_email]):
        print("Email Alert Error: Check email settings in .env")
        return False

    current_price = convert_price(product.get("price"))
    target_price = convert_price(product.get("target_price"))

    if current_price is None or target_price is None:
        print("Email Alert Skipped: Price unavailable")
        return False

    if current_price > target_price:
        print("No Email Alert: Target price not reached")
        return False

    product_name = product.get("name", "Amazon Product")
    product_url = product.get("product_url", "")

    message = EmailMessage()
    message["Subject"] = f"Price Alert: {product_name}"
    message["From"] = sender_email
    message["To"] = receiver_email

    message.set_content(
        f"""Good news!

Your Amazon product has reached its target price.

Product: {product_name}
Current Price: {current_price:g}
Target Price: {target_price:g}

Product URL: {product_url}

Amazon Product Tracker Pro
"""
    )

    try:
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, timeout=30
        ) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)

        print(f"Email Alert Sent: {product_name}")
        return True

    except (smtplib.SMTPException, OSError) as error:
        print(f"Email Alert Failed: {error}")
        return False


def check_and_send_price_alert(product):
    """Send once per target-price cycle; reset when price rises above target."""
    current_price = convert_price(product.get("price"))
    target_price = convert_price(product.get("target_price"))

    if current_price is None or target_price is None:
        print("Email Alert Skipped: Price unavailable")
        return False

    product_key = (
        product.get("product_url")
        or product.get("name")
        or "unknown_product"
    )

    history = load_alert_history()
    was_alerted = history.get(product_key, False)

    if current_price > target_price:
        if was_alerted:
            history[product_key] = False
            save_alert_history(history)

        print("No Email Alert: Target price not reached")
        return False

    if was_alerted:
        print("Duplicate Alert Skipped: Already notified")
        return False

    if send_price_alert(product):
        history[product_key] = True
        save_alert_history(history)
        return True

    return False
