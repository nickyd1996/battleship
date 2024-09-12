import gspread 
from google.oauth2.service_account import Credentials
from flask import Flask, render_template, request, jsonify
import random

#Google Sheets Setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = 'creds.json'  
SPREADSHEET_NAME = 'Battleships'  

credentials = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)
sheet = client.open(SPREADSHEET_NAME).sheet1


#Flask app
app = Flask(__name__)

BOARD_SIZE = 5

#initialize the board in Google Sheets
def initialize_board():
    for i in range(1, BOARD_SIZE + 1):
        for j in range(1, BOARD_SIZE + 1):
            sheet.update_cell(i, j, "")  # Clear the grid

# Place 3 ships randomly on the board
    ships = 0
    while ships < 3:
        x = random.randint(1, BOARD_SIZE)
        y = random.randint(1, BOARD_SIZE)
        if sheet.cell(x, y).value == "":
            sheet.update_cell(x, y, "S")
            ships += 1

# Function to check the result of an attack
def check_attack(x, y):
    cell_value = sheet.cell(x, y).value
    if cell_value == "S":
        sheet.update_cell(x, y, "X")  # Mark hit
        return "hit"
    elif cell_value == "":
        sheet.update_cell(x, y, "O")  # Mark miss
        return "miss"
    return "already attacked"

# Route to initialize the game
@app.route('/initialize', methods=['GET'])
def initialize():
    initialize_board()
    return "Game Initialized!"

# Route to handle the attack
@app.route('/attack', methods=['POST'])
def attack():
    data = request.json
    x = int(data['x'])
    y = int(data['y'])
    result = check_attack(x, y)
    return jsonify({"result": result})

# Main route for the game
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)