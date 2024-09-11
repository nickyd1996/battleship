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

import random

def initialize_board():
    for i in range(1, BOARD_SIZE + 1):
        for j in range(1, BOARD_SIZE + 1):
            sheet.update_cell(i, j, "")  # Clear the grid

    # Randomly place 3 ships
    ships = 0
    while ships < 3:
        x = random.randint(1, BOARD_SIZE)
        y = random.randint(1, BOARD_SIZE)
        if sheet.cell(x, y).value == "":
            sheet.update_cell(x, y, "S")
            ships += 1

def check_attack(x, y):
    cell_value = sheet.cell(x, y).value
    if cell_value == "S":
        sheet.update_cell(x, y, "X")  # Mark hit
        return "hit"
    elif cell_value == "":
        sheet.update_cell(x, y, "O")  # Mark miss
        return "miss"
    return "already attacked"

@app.route('/attack', methods=['POST'])
def attack():
    data = request.json
    x = int(data['x'])
    y = int(data['y'])
    result = check_attack(x, y)
    return jsonify({"result": result})