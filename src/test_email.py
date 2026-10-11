
from email_alert import send_price_alert

# Dummy product used only to test the email system.
# No Amazon scraping is performed by this file.
test_product = {
    "name": "TEST PRODUCT - Email Alert Test",
    "price": "100",
    "target_price": 200,
    "product_url": "https://example.com/test"
}

print("Testing Gmail price alert...")

success = send_price_alert(test_product)

if success:
    print("SUCCESS: Test email sent. Check your inbox.")
else:
    print("FAILED: Check the error message and .env settings.")
