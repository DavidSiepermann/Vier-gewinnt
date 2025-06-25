import random

def create_board():
    """Erstellt ein 6x7 Spielfeld (Liste von Listen) und initialisiert alle Zellen mit 0."""
    board = [[0] * 7 for _ in range(6)]
    return board

def print_board(board):
    """Zeigt das aktuelle Spielfeld im Terminal an."""
    # Spaltennummern oberhalb des Bretts
    print("  " + "   ".join(str(i+1) for i in range(7)))
    for row in board:
        print("| " + " | ".join('X' if cell == 1 else 'O' if cell == 2 else '.' for cell in row) + " |")
    print()  # Leerzeile nach Anzeige

def get_player_move(board, player):
    """Fragt einen gültigen Zug (Spaltennummer 1-7) vom Spieler ab und prüft die Spalte."""
    while True:
        try:
            col = int(input(f"Spieler {player}, wähle Spalte (1-7): ")) - 1
            if col < 0 or col > 6:
                print("Ungültige Spaltennummer. Bitte erneut versuchen.")
            elif board[0][col] != 0:
                print("Diese Spalte ist voll. Wähle eine andere Spalte.")
            else:
                return col
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")

def get_computer_move(board):
    """Ermittelt zufällig eine gültige Spalte für den Computerzug (zufällige Wahl)."""
    valid_cols = [c for c in range(7) if board[0][c] == 0]
    if not valid_cols:
        return None
    return random.choice(valid_cols)

def drop_piece(board, col, piece):
    """Lässt einen Spielstein (1 oder 2) in die angegebene Spalte fallen (falls möglich)."""
    for r in range(5, -1, -1):  # von unten nach oben suchen
        if board[r][col] == 0:
            board[r][col] = piece
            return True
    return False

def check_win(board, piece):
    """Prüft, ob der gegebene Spieler (piece=1 oder 2) vier Steine in einer Reihe hat."""
    # Horizontal prüfen
    for r in range(6):
        for c in range(4):
            if board[r][c] == piece == board[r][c+1] == board[r][c+2] == board[r][c+3]:
                return True
    # Vertikal prüfen
    for c in range(7):
        for r in range(3):
            if board[r][c] == piece == board[r+1][c] == board[r+2][c] == board[r+3][c]:
                return True
    # Diagonal (unten-links nach oben-rechts)
    for r in range(3, 6):
        for c in range(4):
            if board[r][c] == piece == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3]:
                return True
    # Diagonal (oben-links nach unten-rechts)
    for r in range(3):
        for c in range(4):
            if board[r][c] == piece == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]:
                return True
    return False

def is_draw(board):
    """Prüft, ob das Spielfeld voll ist (Unentschieden)."""
    for row in board:
        if 0 in row:
            return False
    return True

def main():
    print("Willkommen zu Vier gewinnt!")
    mode = input("Wähle Spielmodus: 1 - 2 Spieler, 2 - 1 Spieler vs Computer: ")
    while mode not in ("1", "2"):
        mode = input("Ungültig. Bitte 1 oder 2 eingeben: ")
    mode = int(mode)
    board = create_board()
    current_player = 1
    game_over = False

    while not game_over:
        print_board(board)
        if mode == 1 or current_player == 1:
            # Zug von Spieler 1 (bzw. jeder Spieler im 2-Spieler-Modus)
            col = get_player_move(board, current_player)
        else:
            # Computerzug (Spieler 2)
            col = get_computer_move(board)
            if col is None:
                break  # Kein freies Feld mehr
            print(f"Computer wählt Spalte {col+1}.")
        drop_piece(board, col, current_player)

        # Gewinn prüfen
        if check_win(board, current_player):
            print_board(board)
            if mode == 2 and current_player == 2:
                print("Computer hat gewonnen!")
            else:
                print(f"Spieler {current_player} hat gewonnen!")
            game_over = True
        # Unentschieden prüfen
        elif is_draw(board):
            print_board(board)
            print("Unentschieden! Das Spielfeld ist voll.")
            game_over = True
        else:
            current_player = 2 if current_player == 1 else 1

if __name__ == "__main__":
    main()
