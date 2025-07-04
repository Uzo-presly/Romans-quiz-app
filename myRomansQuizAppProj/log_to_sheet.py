import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def log_to_sheet(timestamp, ip_address, email, score, total, browser_info):
    """
    Logs quiz result to a Google Sheet with extra details.
    """
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise Exception("GOOGLE_APPLICATION_CREDENTIALS not set.")

        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_key("1BRGQDn0kSZ9qrznIkl2JoM_qp-5xF_GikcenBM3BXDA").sheet1

        sheet.append_row([timestamp, ip_address, email, score, total, browser_info])
        print(f"✅ Logged to sheet: {timestamp}, {ip_address}, {email}, {score}/{total}, {browser_info}")

    except Exception as e:
        print("❌ Failed to log to sheet:", e)
