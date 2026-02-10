import gspread
from google.oauth2.service_account import Credentials

def get_gspread_client(service_account_path, scope: list[str]):
    credentials = Credentials.from_service_account_file(
        service_account_path,
        scopes=scope
    )
    return gspread.authorize(credentials)