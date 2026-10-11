
from scraper import AmazonScraper
from exporter import (
    export_to_csv,
    export_to_excel,
    save_price_history
)

import time
import random

from logger import log_message
from input_reader import read_products
from email_alert import check_and_send_price_alert



def main():
    log_message("Amazon Product Tracker Started")

    products_to_track = read_products()

    print(f"\nTotal Products Loaded: {len(products_to_track)}")

    if not products_to_track:
        print("No valid Amazon products found.")
        return

    all_products = []
    success_count = 0
    failed_count = 0

    for item in products_to_track:
        url = item["product_url"]
        target_price = item["target_price"]

        print("\n" + "=" * 60)
        print(f"Target Price: {target_price}")
        print(f"URL: {url}")

        scraper = AmazonScraper()

        try:
            product = scraper.get_product_info(url)

            # Excel se aane wali target price attach karo
            product["target_price"] = target_price
            check_and_send_price_alert(product)

            log_message(f"URL: {url}")
            log_message(f"Product: {product['name']}")
            log_message(f"Target Price: {target_price}")

            all_products.append(product)

            if product["name"] in ["Timeout", "Failed"]:
                failed_count += 1
            else:
                success_count += 1

        except Exception as error:
            failed_count += 1

            log_message(f"Error scraping {url}: {error}")

            all_products.append({
                "name": "Failed",
                "price": "Not Found",
                "rating": "Not Found",
                "availability": "Unknown",
                "product_url": url,
                "target_price": target_price
            })

        finally:
            scraper.close()

        time.sleep(random.randint(3, 7))

    print("\n" + "=" * 60)
    print("TRACKING SUMMARY")
    print("=" * 60)

    print(f"Total Products : {len(products_to_track)}")
    print(f"Successful     : {success_count}")
    print(f"Failed         : {failed_count}")

    export_to_csv(all_products)
    log_message("CSV Export Completed")

    export_to_excel(all_products)
    log_message("Excel Export Completed")

    save_price_history(all_products)
    log_message("Price History Updated")

    log_message(
        f"Tracking Summary - Total: {len(products_to_track)}, "
        f"Success: {success_count}, Failed: {failed_count}"
    )

    log_message("Amazon Product Tracker Finished")


if __name__ == "__main__":
    main()
