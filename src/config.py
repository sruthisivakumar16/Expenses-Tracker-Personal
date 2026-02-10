from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
SERVICE_ACCOUNT_JSON_PATH = os.getenv("SERVICE_ACCOUNT_JSON_PATH", "service_account.json")
SCOPE = os.getenv("SCOPE", "https://www.googleapis.com/auth/spreadsheets")
