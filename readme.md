# anonymize-sales

A Python script to anonymize Depop sales CSVs and export the results to Google Sheets. It removes personally identifiable information (PII) and hashes sensitive columns.

---

## Features

- Removes PII columns Name, Address1 & 2, City, and Post Code  
- Hashes sensitive column Buyer with SHA-256
- Cleans invalid or missing data  
- Uploads the anonymized data directly to Google Sheets based on spreadsheet key

---

## Requirements

- Python 3.8+  
- Packages listed in `requirements.txt`:

## To use:
1. Clone the repository
2. Install dependencies:

pip install -r requirements.txt
3. Create a `.env` file with your credentials:

CRED_FILE=path/to/service_account.json

SPREADSHEET_ID=your_google_sheet_id