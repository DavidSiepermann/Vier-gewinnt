import random
import math

# Spielfeldgrößen
ROWS = 6
COLS = 7

# Spielfiguren
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

# Minimax-Konfiguration
WINDOW_LENGTH = 4
DEPTH = 4  # Maximale Tiefe für Minimax

# Spielfeld erstellen
def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

# Spielfeld anzeigen
def print_board(board):
    print("  " + "   ".join(str(i+1) for i in range(COLS)))
    for row in board:
        print("| " + " | ".join('X' if cell == PLAYER_PIECE else 'O' if cell == AI_PIECE else '.' for cell in row) + " |")
    print()

# Stein setzen
def drop_piece(board, col, piece):
    for r in reversed(range(ROWS)):
        if board[r][col] == EMPTY:
            board[r][col] = piece
            return

# Gültige Züge
def get_valid_locations(board):
    return [c for c in range(COLS) if board[0][c] == EMPTY]

def is_valid_location(board, col):
    return board[0][col] == EMPTY

# Gewinn prüfen
def check_win(board, piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Vertikal
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Diagonal /
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # Diagonal \
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

# Unentschieden prüfen
def is_draw(board):
    return all(cell != EMPTY for cell in board[0])

# Bewertungsfunktion
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score

# Gesamtbewertung
def score_position(board, piece):
    score = 0
    # Zentrum bevorzugen
    center_array = [board[r][COLS//2] for r in range(ROWS)]
    score += center_array.count(piece) * 3
    # Horizontal
    for r in range(ROWS):
        row_array = board[r]
        for c in range(COLS - 3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Vertikal
    for c in range(COLS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Diagonalen
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score

# Terminalzustand prüfen
def is_terminal_node(board):
    return check_win(board, PLAYER_PIECE) or check_win(board, AI_PIECE) or is_draw(board)

# Minimax mit Alpha-Beta
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, AI_PIECE):
                return (None, float('inf'))
            elif check_win(board, PLAYER_PIECE):
                return (None, float('-inf'))
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = float('-inf')
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, col, AI_PIECE)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = float('inf')
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, col, PLAYER_PIECE)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

# Spieler-Zug
def get_player_move(board):
    while True:
        try:
            col = int(input("Wähle eine Spalte (1-7): ")) - 1
            if 0 <= col <= 6 and is_valid_location(board, col):
                return col
            else:
                print("Ungültiger Zug.")
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")

# Spielstart
def main():
    print("Willkommen zu Vier gewinnt!")
    print("Modus wählen: 1 - Zwei Spieler, 2 - Spieler gegen KI")
    mode = input("Eingabe: ")
    while mode not in ("1", "2"):
        mode = input("Bitte 1 oder 2 eingeben: ")

    board = create_board()
    game_over = False
    turn = 0  # 0 = Spieler 1, 1 = Spieler 2 / KI

    while not game_over:
        print_board(board)

        if mode == "1" or turn == 0:
            col = get_player_move(board)
        else:
            print("Computer denkt...")
            col, _ = minimax(board, DEPTH, -math.inf, math.inf, True)
            print(f"Computer wählt Spalte {col+1}")


        piece = PLAYER_PIECE if turn == 0 else AI_PIECE if mode == "2" else 2

        if is_valid_location(board, col):
            drop_piece(board, col, piece)
            if check_win(board, piece):
                print_board(board)
                if mode == "2" and turn == 1:
                    print("Computer gewinnt!")
                else:
                    print(f"Spieler {piece} gewinnt!")
                game_over = True
            elif is_draw(board):
                print_board(board)
                print("Unentschieden!")
                game_over = True
            turn ^= 1  # Spieler wechseln

if __name__ == "__main__":
    main()
