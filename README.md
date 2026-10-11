# Amazon Product Tracker Pro 🛒

A Python-based Amazon product tracking tool built with Selenium. It collects product information, tracks prices, exports data to CSV and Excel, and sends email alerts when a product reaches or falls below its target price.

## ✨ Features

- **Product Scraping:** Extract product names, prices, ratings, and availability.
- **Multiple Products:** Process multiple Amazon product URLs from an Excel input file.
- **Target Price Tracking:** Compare current prices with user-defined target prices.
- **Email Alerts:** Receive email notifications when a product reaches its target price.
- **Duplicate Alert Prevention:** Avoid repeatedly sending the same alert while the price remains below the target.
- **CSV Export:** Save collected product data to CSV.
- **Excel Export:** Export product data to Excel.
- **Price History:** Maintain a history of tracked product prices.
- **Logging:** Record scraper activity and errors.
- **Error Handling:** Handle scraping issues and unavailable product information.

## 🛠️ Technologies Used

- Python
- Selenium
- pandas
- openpyxl
- python-dotenv
- Chrome WebDriver

## 📁 Project Structure

```text
Amazon Product Tracker Pro/
├── input/
│   └── products.xlsx
├── output/                  # Generated files
├── logs/                    # Runtime logs
├── src/
│   ├── main.py
│   ├── scraper.py
│   ├── exporter.py
│   ├── input_reader.py
│   ├── email_alert.py
│   ├── logger.py
│   └── test_email.py
├── .env                     # Private credentials; do not upload
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/MuneebAITech/Python-Amazon-Product-Tracker-Pro.git
cd Python-Amazon-Product-Tracker-Pro
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```cmd
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the input Excel file

Open `input/products.xlsx` and add these columns:

| product_url | target_price |
|---|---:|
| https://www.amazon.com/dp/PRODUCT_ID | 3000 |
| https://www.amazon.com/dp/ANOTHER_PRODUCT_ID | 5000 |

Replace the example URLs and prices with the products you want to track. Use valid product-detail URLs for your chosen Amazon marketplace.

### 5. Configure email alerts

Create a `.env` file in the project root:

```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password
RECEIVER_EMAIL=recipient@gmail.com
```

Use a Gmail App Password where required, not your regular Gmail password. Keep `.env` private and never commit it to GitHub.

## ▶️ Run the Project

From the project root, with your virtual environment activated, run:

```bash
python src/main.py
```

The program reads products from Excel, attempts to collect their information, checks target prices, sends eligible email alerts, and exports the results.

## 📊 Output Files

Generated files may include:

- `output/products.csv` — scraped product data in CSV format.
- `output/products.xlsx` — scraped product data in Excel format.
- `output/price_history.csv` — historical price records.
- `output/alert_history.json` — records used to prevent repeated alerts.
- `logs/scraper.log` — scraper activity and diagnostic information.

These files are generated locally and are excluded from version control.

## ⚠️ Important Notes

- Amazon page layouts, regional availability, bot checks, and rate limits can affect scraping results.
- Prices and product availability may be missing or inaccurate if Amazon changes its page structure.
- Use reasonable request delays and comply with applicable website terms and policies.
- This project is intended for educational purposes and Python automation practice. It does not guarantee uninterrupted access to Amazon data.

## 👨‍💻 Author

**MuneebAITech**

GitHub: https://github.com/MuneebAITech

## 📄 License

Choose and add a license before distributing or reusing this project publicly.
