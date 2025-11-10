"""
A Python script meant to anonymize sales data by removing personally identifiable information (PII) from a CSV file.
The script reads a CSV file, removes specified PII columns, and saves the anonymized data to a new CSV file.
"""

import pandas as pd
import hashlib
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from dotenv import load_dotenv
import os

load_dotenv()

CRED_FILE = os.getenv("CRED_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


def choose_file():
    # tkinter file dialog to choose a file
    Tk().withdraw()
    file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        raise FileNotFoundError("No file selected.")
    return file_path



def read_sales_data(file_path):
    return pd.read_csv(file_path)


def clean_df(df):
    # cleans the DataFrame by replacing infinite values and filling NaNs
    df = df.replace([float('inf'), float('-inf')], pd.NA)
    df = df.fillna("")
    return df



def anonymize_sales_data(df, pii_columns):
    # drops PII columns
    df = df.copy()
    df.drop(columns=pii_columns, errors='ignore', inplace=True)
    return df




def hash_pii_columns(df, pii_columns):
    # hashes PII columns
    df = df.copy()
    for col in pii_columns:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: hashlib.sha256(str(x).encode()).hexdigest() if pd.notnull(x) else x
            )
    return df


def upload_to_google_sheet(df, sheet_id, creds_file=CRED_FILE):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
    gs_client = gspread.authorize(creds)

    try:
        spreadsheet = gs_client.open_by_key(sheet_id)
    except gspread.SpreadsheetNotFound:
        raise FileNotFoundError("Spreadsheet not found. Check the SPREADSHEET_ID.")

    worksheet = spreadsheet.sheet1
    worksheet.clear()
    set_with_dataframe(worksheet, df)




def main():
    df = read_sales_data(choose_file())
    df = clean_df(df)

    pii_columns_to_remove = ["Name", "Address Line 1", "Address Line 2", "City", "Post Code", "Buyer"]
    if pii_columns_to_remove:
        df = anonymize_sales_data(df, pii_columns_to_remove)

    hash_columns = []
    if hash_columns
        df = hash_pii_columns(df, hash_columns)


    upload_to_google_sheet(df, sheet_id=SPREADSHEET_ID, creds_file=CRED_FILE)
    print("Upload to Google Sheets completed.")

if __name__ == "__main__":
    main()