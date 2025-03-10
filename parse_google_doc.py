import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import timedelta

# Google Sheets Configuration
SPREADSHEET_ID = "YOUR_GOOGLE_SHEET_ID"  # Replace with the studio sheet
SHEET_NAME = "Form_Responses1"
GOOGLE_CREDENTIALS_FILE = "youtube_service_account.json"

def get_google_sheet():
    """Fetch Google Sheet data and process it."""
    try:
        # Authenticate with Google Sheets API
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)

        # Load sheet data
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        # Clean column names
        df.columns = df.columns.str.strip().str.replace('\n', ' ')

        # Convert date and time columns
        df['Date of Show'] = pd.to_datetime(df['Date of Show'], errors="coerce")
        df['Start Time'] = pd.to_datetime(df['Start Time'], format='%I:%M:%S %p', errors="coerce").dt.time
        
        # Create full datetime column
        df['Show datetime'] = pd.to_datetime(df['Date of Show'].astype(str) + ' ' + df['Start Time'].astype(str))
        
        # Add columns for 30 minutes before/after
        df['30m before'] = df['Show datetime'] - timedelta(minutes=30)
        df['30m after'] = df['Show datetime'] + timedelta(minutes=30)

        return df
    except Exception as e:
        print(f" Error fetching Google Sheets data: {e}")
        return None