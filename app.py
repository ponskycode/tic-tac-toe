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


# Endpoint do wysyłania ruchu
@app.route('/move', methods=['POST'])
def move():
    data = request.json
    # Zrobimy prostą logikę, która przyjmie ruch gracza
    # (można tu dodać logikę sprawdzania, kto wygrał)
    return jsonify({'message': 'Move accepted', 'board': data['board']})


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
