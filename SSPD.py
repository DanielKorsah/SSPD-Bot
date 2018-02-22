
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

# authorisation to access google sheet
scope = ["https://spreadsheets.google.com/feeds"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "client_secret.json", scope)
gc = gspread.authorize(creds)
client = gspread.authorize(creds)

# initialise the sheet
sheet = gc.open("Warnings List").sheet1
warnings = sheet.row_values(4)

# remove empty cells
warnings = list(filter(lambda x: x != '', warnings))

pp = pprint.PrettyPrinter()
print(warnings)
