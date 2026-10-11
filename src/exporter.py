
import pandas as pd
import os
from datetime import datetime


OUTPUT_DIR = "output"


def prepare_output_folder():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def prepare_products(products):
    """Prepare product data and compare current price with target price."""
    prepared = []

    for product in products:
        item = product.copy()

        current_price = item.get("price")
        target_price = item.get("target_price")

        # Convert prices to numbers where possible
        try:
            if current_price is not None:
                current_price = float(
                    str(current_price).replace(",", "").replace("$", "").strip()
                )
            else:
                current_price = None
        except (ValueError, TypeError):
            current_price = None

        try:
            if target_price is not None:
                target_price = float(target_price)
            else:
                target_price = None
        except (ValueError, TypeError):
            target_price = None

        item["current_price"] = current_price
        item["target_price"] = target_price

        if current_price is None:
            item["target_status"] = "Price Unavailable"
        elif target_price is None:
            item["target_status"] = "No Target Set"
        elif current_price <= target_price:
            item["target_status"] = "Target Reached"
        else:
            item["target_status"] = "Target Not Reached"

        prepared.append(item)

    return prepared


def export_to_csv(products):
    prepare_output_folder()

    products = prepare_products(products)
    df = pd.DataFrame(products)

    df.to_csv(
        os.path.join(OUTPUT_DIR, "products.csv"),
        index=False
    )

    print("\nCSV File Saved Successfully")


def export_to_excel(products):
    prepare_output_folder()

    products = prepare_products(products)
    df = pd.DataFrame(products)

    df.to_excel(
        os.path.join(OUTPUT_DIR, "products.xlsx"),
        index=False
    )

    print("Excel File Saved Successfully")


def save_price_history(products):
    prepare_output_folder()

    history_file = os.path.join(
        OUTPUT_DIR, "price_history.csv"
    )

    products = prepare_products(products)
    df = pd.DataFrame(products)

    df["date"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    if os.path.exists(history_file):
        df.to_csv(
            history_file,
            mode="a",
            header=False,
            index=False
        )
    else:
        df.to_csv(
            history_file,
            index=False
        )

    print("Price History Updated")
