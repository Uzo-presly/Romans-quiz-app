import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def log_to_sheet(email, score, total):
    try:
        # Path to your .json key file
        SERVICE_ACCOUNT_FILE = "myRomansQuizAppProj/.secrets/true-oasis-449208-c6-27acdba00e47.json"

        # Define scope
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        # Authenticate using modern google-auth library
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)

        # Open Google Sheet by name
        sheet = client.open("Romans2QuizLogger").sheet1

        # Append the result
        sheet.append_row([email, score, total, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        print(f"✅ Logged to sheet: {email}, {score}/{total}")

    except Exception as e:
        print("❌ Failed to log to sheet:", e)
