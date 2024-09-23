# Tic-tac-toe
A simple web app where you play tic-tac-toe

## Diagram klas

Diagram klas dla aplikacji zawiera jedną klasę Player, która odpowiada za przechowywanie informacji o graczach.

Klasa: Player

    Atrybuty:
        id: int – klucz główny.
        username: str – unikalna nazwa użytkownika (gracza).
        ilosc_wynikow: int – liczba rozegranych gier.
        ilosc_remisow: int – liczba remisów.
        ilosc_wygranych: int – liczba wygranych gier.

## Diagram bazy danych

W bazie danych SQLite dla tej aplikacji znajduje się jedna tabela o nazwie Player.
Tabela Player
Kolumna | Typ danych | Opis
:---: | :---: | :---: 
id | INTEGER | Klucz główny (autoincrement).
username | VARCHAR(50) | Unikalna nazwa gracza.
ilosc_wynikow | INTEGER | Liczba rozegranych gier.
ilosc_remisow | INTEGER | Liczba remisów.
ilosc_wygranych | INTEGER | Liczba wygranych gier.

    Tabela ta przechowuje dane na temat wyników graczy, ich remisów oraz wygranych.
    Nie ma relacji między tabelami, gdyż aplikacja posiada tylko jedną tabelę.

# Opis endpointów
1. GET /

    Opis: Renderuje stronę startową, gdzie gracz może wprowadzić swój pseudonim.
   
    Odpowiedź: Strona HTML.

3. GET /game

    Opis: Renderuje stronę z planszą do gry w kółko i krzyżyk.
   
    Odpowiedź: Strona HTML zawierająca planszę i leaderboard.

5. POST /new_game

    Opis: Rozpoczyna nową grę.
   
    Body (JSON): { "playerName": "nazwa_gracza" }
   
    Odpowiedź (JSON): { "message": "New game started!" }

7. POST /move

    Opis: Przesyła ruch gracza i obsługuje całą logikę gry (w tym ruch komputera).
   
    Body (JSON):

        {
          "board": ["X", "", "", "O", "", "", "", "", ""],
          "moveIndex": 1,
          "playerName": "nazwa_gracza"
        }

    Odpowiedzi (JSON):
    
    Gracz wygrywa:
    
        {
          "message": "nazwa_gracza wins!",
          "board": [...],
          "gameOver": true
        }
    
    Komputer wygrywa:
    
        {
          "message": "Komputer wins!",
          "board": [...],
          "gameOver": true
        }
    
    Remis:
    
        {
          "message": "It's a draw!",
          "board": [...],
          "gameOver": true
        }
    
    Gra trwa dalej:
    
       {
         "message": "Move accepted",
         "board": [...],
         "gameOver": false
       }

5. GET /leaderboard

    Opis: Zwraca wyniki graczy posortowane po liczbie wygranych gier.
   
    Odpowiedź (JSON):

        [
          { "username": "player1", "ilosc_wygranych": "5", "ilosc_remisow": "2", "ilosc_wynikow": "7" },
          { "username": "player2", "ilosc_wygranych": "3", "ilosc_remisow": "1", "ilosc_wynikow": "4" }
        ]

## Diagram klas i diagram bazy danych

1. Diagram klas:

   Klasa Player posiada atrybuty id, username, ilosc_wynikow, ilosc_remisow, i ilosc_wygranych.
   
3. Diagram bazy danych:

   Tabela Player zawiera kolumny odpowiadające atrybutom klasy Player.
