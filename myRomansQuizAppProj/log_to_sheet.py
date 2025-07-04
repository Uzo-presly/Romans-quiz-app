import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

        # Try Render deployment path first, fall back to local path
        json_path = "/etc/secrets/true-oasis-449208-c6-27acdba00e47.json"
        if not os.path.exists(json_path):
            json_path = ".secrets/true-oasis-449208-c6-27acdba00e47.json"

        creds = ServiceAccountCredentials.from_json_keyfile_name(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1BRGQDn0kSZ9qrznIkl2JoM_qp-5xF_GikcenBM3BXDA").sheet1

        sheet.append_row([timestamp, ip_address, email, score, total, browser_info])
        print(f"✅ Logged to sheet: {timestamp}, {ip_address}, {email}, {score}/{total}, {browser_info}")

    except Exception as e:
        print("❌ Failed to log to sheet:", e)
