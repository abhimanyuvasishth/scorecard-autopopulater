import gspread
from gspread.worksheet import Worksheet
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet(Worksheet):
    def __new__(cls, doc_name, sheet_name, *args, **kwargs):
        scope = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        file = 'credentials.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(file, scope)
        client = gspread.authorize(creds)
        return client.open(doc_name).worksheet(sheet_name)
