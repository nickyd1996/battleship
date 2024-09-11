import gspread 
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('battleships')
info = SHEET.worksheet('info')


from flask import Flask, render_template

app = Flask(__name__)

BOARD_SIZE = 5

def initialize_board():
    for i in range(1, BOARD_SIZE + 1):
        for j in range(1, BOARD_SIZE + 1):
            info.update_cell(i, j, "")  # Clear the grid

@app.route('/initialize')
def initialize():
    initialize_board()
    return "Board initialized"