from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tic_tac_toe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model gracza (do przechowywania wyników)
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    ilosc_wynikow = db.Column(db.Integer, default=0)  # Liczba rozegranych gier
    ilosc_remisow = db.Column(db.Integer, default=0)  # Liczba remisów
    ilosc_wygranych = db.Column(db.Integer, default=0)  # Liczba wygranych

    def __repr__(self):
        return f'<Player {self.username}>'

# Endpoint dla strony startowej (formularz do wpisania nicku)
@app.route('/')
def start():
    return render_template('start.html')

# Endpoint do strony gry
@app.route('/game')
def game():
    return render_template('index.html')

# Endpoint do rozpoczęcia nowej gry
@app.route('/new_game', methods=['POST'])
def new_game():
    return jsonify({'message': 'New game started!'})

# Funkcja do sprawdzenia, czy jest wygrana
def check_winner(board):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        a, b, c = condition
        if board[a] == board[b] == board[c] and board[a] != '':
            return board[a]
    return None

# Funkcja do ruchu komputera
def computer_move(board):
    available_moves = [i for i, spot in enumerate(board) if spot == '']
    if available_moves:
        move = random.choice(available_moves)
        board[move] = 'O'
    return board

# Endpoint do wysyłania ruchu
@app.route('/move', methods=['POST'])
def move():
    data = request.json
    board = data['board']
    move_index = data['moveIndex']
    player_name = data['playerName']  # Pobieramy nazwę gracza
    
    # Szukamy gracza w bazie danych
    player = Player.query.filter_by(username=player_name).first()
    
    # Jeśli gracza nie ma w bazie, dodajemy go
    if not player:
        player = Player(username=player_name)
        db.session.add(player)
        db.session.commit()
    
    if board[move_index] == '':
        board[move_index] = 'X'  # Gracz X wykonuje ruch

    # Sprawdzamy, czy gracz wygrał
    winner = check_winner(board)
    if winner:
        player.ilosc_wynikow += 1  # Zwiększamy liczbę rozegranych gier
        if winner == 'X':
            player.ilosc_wygranych += 1  # Zwiększamy liczbę wygranych
            db.session.commit()
            return jsonify({'message': f'{player_name} wins!', 'board': board, 'gameOver': True})
        elif winner == 'O':
            db.session.commit()  # Komputer wygrał, więc tylko zapisujemy grę
            return jsonify({'message': 'Komputer wins!', 'board': board, 'gameOver': True})

    # Jeśli nie ma wygranego, komputer wykonuje ruch
    board = computer_move(board)

    # Sprawdzamy, czy komputer wygrał po swoim ruchu
    winner = check_winner(board)
    if winner:
        player.ilosc_wynikow += 1  # Zwiększamy liczbę rozegranych gier
        if winner == 'O':
            db.session.commit()  # Komputer wygrał, tylko zapisujemy
            return jsonify({'message': 'Komputer wins!', 'board': board, 'gameOver': True})

    # Sprawdzamy, czy jest remis
    if '' not in board:
        player.ilosc_wynikow += 1  # Zwiększamy liczbę rozegranych gier
        player.ilosc_remisow += 1  # Zwiększamy liczbę remisów
        db.session.commit()
        return jsonify({'message': 'It\'s a draw!', 'board': board, 'gameOver': True})

    db.session.commit()  # Zapisujemy stan gry, jeśli gra się toczy dalej
    return jsonify({'message': 'Move accepted', 'board': board, 'gameOver': False})

# Endpoint do wyświetlania wyników
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    players = Player.query.order_by(Player.ilosc_wygranych.desc()).all()  # Sortowanie po liczbie wygranych
    results = [{'username': player.username, 'ilosc_wygranych': str(player.ilosc_wygranych), 'ilosc_remisow': str(player.ilosc_remisow), 'ilosc_wynikow': str(player.ilosc_wynikow)} for player in players]
    return jsonify(results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzenie tabel w bazie danych
    app.run(debug=True)
