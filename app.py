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
    wins = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Player {self.username}>'


# Endpoint do renderowania strony głównej
@app.route('/')
def index():
    return render_template('index.html')


# Endpoint do rozpoczęcia nowej gry
@app.route('/new_game', methods=['POST'])
def new_game():
    # Dane mogą pochodzić z requestu, np. gracze, tryb itp.
    return jsonify({'message': 'New game started!'})

# Funkcja do sprawdzenia, czy jest wygrana
def check_winner(board):
    # Sprawdzanie wygrywających kombinacji
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
    
    # Aktualizuj planszę po ruchu użytkownika
    if board[move_index] == '':
        board[move_index] = 'X'  # Gracz X wykonuje ruch

    # Sprawdzamy, czy gracz X wygrał po swoim ruchu
    winner = check_winner(board)
    if winner:
        return jsonify({'message': f'Player {winner} wins!', 'board': board, 'gameOver': True})

    # Jeśli nie ma wygranego, komputer wykonuje ruch
    board = computer_move(board)

    # Sprawdzamy, czy komputer wygrał po swoim ruchu
    winner = check_winner(board)
    if winner:
        return jsonify({'message': f'Player {winner} wins!', 'board': board, 'gameOver': True})

    # Sprawdzamy, czy jest remis (brak pustych pól)
    if '' not in board:
        return jsonify({'message': 'It\'s a draw!', 'board': board, 'gameOver': True})

    return jsonify({'message': 'Move accepted', 'board': board, 'gameOver': False})

# Endpoint do zapisywania wyników
@app.route('/save_result', methods=['POST'])
def save_result():
    data = request.json
    username = data.get('username')
    player = Player.query.filter_by(username=username).first()
    if player:
        player.wins += 1
    else:
        player = Player(username=username, wins=1)
        db.session.add(player)
    db.session.commit()
    return jsonify({'message': 'Result saved!'})


# Endpoint do wyświetlania wyników
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    players = Player.query.order_by(Player.wins.desc()).all()
    results = [{'username': player.username, 'wins': player.wins} for player in players]
    return jsonify(results)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzenie tabel w bazie danych
    app.run(debug=True)
