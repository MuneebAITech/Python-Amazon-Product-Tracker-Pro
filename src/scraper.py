from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)


class AmazonScraper:

    def __init__(self):

        user_agents = [

            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36",

            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36",

            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"
        ]


        options = webdriver.ChromeOptions()

        selected_agent = random.choice(
            user_agents
        )

        options.add_argument(
            f"user-agent={selected_agent}"
        )

        print(
            f"\nUser Agent Loaded"
        )
        print(selected_agent)

        # options.add_argument(
        #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        # )

        options.add_argument("--start-maximized")

        options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation"]
        )

        options.add_experimental_option(
            "useAutomationExtension",
            False
        )

        self.driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=options
        )

        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def get_product_info(self, url):

        max_retries = 3

        try:
            self.driver.set_page_load_timeout(30)
            max_retries = 3

            for attempt in range(max_retries):

                try:

                    self.driver.set_page_load_timeout(30)

                    self.driver.get(url)

                    time.sleep(
                        random.randint(2, 4)
                    )

                    self.driver.execute_script(
                        "window.scrollTo(0, 600);"
                    )

                    time.sleep(
                        random.randint(1, 3)
                    )

                    self.driver.execute_script(
                        "window.scrollTo(0, 0);"
                    )

                    time.sleep(
                        random.randint(1, 2)
                    )

                    print(
                        "Human Behavior Simulated"
                    )

                    break


                except TimeoutException:

                    print(
                        f"\nTimeout Attempt {attempt + 1}"
                    )

                    time.sleep(5)

            else:

                print("\nAll Retries Failed")

                return {
                    "name": "Timeout",
                    "price": "N/A",
                    "rating": "N/A",
                    "availability": "N/A"
                }

            

        except TimeoutException:

            print("\nPage Load Timeout")
            
            return {
                "name": "Timeout",
                "price": "N/A",
                "rating": "N/A",
                "availability": "N/A"
            }

        try:

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.ID, "productTitle")
                )
            )

        except TimeoutException:

            print("\nProduct Title Not Found")

            print("Current URL:", self.driver.current_url)
            
            print("Page Title :", self.driver.title)

            return {
                "name": "Timeout",
                "price": "N/A",
                "rating": "N/A",
                "availability": "N/A"
            }

        

        # Product Name
        try:
            title = self.driver.find_element(
                By.ID,
                "productTitle"
            ).text.strip()

        except:
            title = "Not Found"

        # Product Price
        try:
            price = self.driver.find_element(
                By.CLASS_NAME,
                "a-price-whole"
            ).text.strip()

        except:
            price = "Not Found"

        # Product Rating
        try:
            rating_element = self.driver.find_element(
                By.CSS_SELECTOR,
                "span.a-icon-alt"
            )

            rating = rating_element.get_attribute("textContent").strip()

            if not rating:
                rating = rating_element.get_attribute("innerHTML").strip()

        except:
            rating = "Not Found"

        # Availability
        try:
            availability = self.driver.find_element(
                By.ID,
                "availability"
            ).text.strip()

        except:
            availability = "Not Found"

        product = {
            "name": title,
            "price": price,
            "rating": rating,
            "availability": availability
        }

        print(f"\nProduct Name : {title}")
        print(f"Price        : {price}")
        print(f"Rating       : {rating}")
        print(f"Availability : {availability}")

        return product

    def close(self):
        self.driver.quit()

