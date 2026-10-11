
import pandas as pd
from pathlib import Path


def read_products():
    # Project root folder
    project_dir = Path(__file__).resolve().parent.parent
    excel_file = project_dir /  "input" / "products.xlsx"

    if not excel_file.exists():
        raise FileNotFoundError(
            f"Excel file not found: {excel_file}"
        )

    df = pd.read_excel(excel_file)

    # Column names ke extra spaces remove karo
    df.columns = df.columns.str.strip().str.lower()

    required_columns = {"product_url", "target_price"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing Excel columns: {', '.join(missing_columns)}"
        )

    # Empty URLs remove karo
    df = df.dropna(subset=["product_url"])
    df["product_url"] = df["product_url"].astype(str).str.strip()
    df = df[df["product_url"] != ""]

    # Blank target prices ko None rakho
    df["target_price"] = df["target_price"].where(
        pd.notna(df["target_price"]), None
    )

    products = df[["product_url", "target_price"]].to_dict(
        orient="records"
    )

    return products


if __name__ == "__main__":
    products = read_products()

    print(f"Total products loaded: {len(products)}")

    for product in products:
        print(product)
