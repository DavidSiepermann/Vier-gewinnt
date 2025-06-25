import random

ROWS = 6
COLUMNS = 7

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
    print('  ' + '   '.join(map(str, range(COLUMNS))))

def make_move(board, col, symbol):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col
    return None  # Spalte voll

def is_valid_move(board, col):
    return 0 <= col < COLUMNS and board[0][col] == ' '

def switch_player(symbol):
    return 'O' if symbol == 'X' else 'X'

def check_win(board, row, col, symbol):
    def count_dir(delta_row, delta_col):
        count = 0
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
            count += 1
            r += delta_row
            c += delta_col
        return count

    directions = [(1,0), (0,1), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1 + count_dir(dr, dc) + count_dir(-dr, -dc)
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def get_human_move(board):
    while True:
        try:
            col = int(input("Wähle eine Spalte (0-6): "))
            if is_valid_move(board, col):
                return col
            else:
                print("Ungültige Spalte. Bitte erneut versuchen.")
        except ValueError:
            print("Bitte gib eine Zahl ein.")

def get_computer_move(board, computer_symbol, human_symbol):
    # 1. Gewinnzug suchen
    for col in range(COLUMNS):
        if is_valid_move(board, col):
            temp_board = [row[:] for row in board]
            row_col = make_move(temp_board, col, computer_symbol)
            if row_col and check_win(temp_board, row_col[0], row_col[1], computer_symbol):
                return col

    # 2. Blockiere gegnerischen Gewinn
    for col in range(COLUMNS):
        if is_valid_move(board, col):
            temp_board = [row[:] for row in board]
            row_col = make_move(temp_board, col, human_symbol)
            if row_col and check_win(temp_board, row_col[0], row_col[1], human_symbol):
                return col

    # 3. Zentrum bevorzugen
    if is_valid_move(board, 3):
        return 3

    # 4. Sonst bestmöglicher Zug aus gültigen Zügen (leicht smartere Zufallswahl)
    valid_moves = [c for c in range(COLUMNS) if is_valid_move(board, c)]
    preferred = [3, 2, 4, 1, 5, 0, 6]  # Spalten nach Nähe zur Mitte
    for col in preferred:
        if col in valid_moves:
            return col

def play_game():
    print("Willkommen bei Vier Gewinnt!")

    # Spielmodus wählen
    print("Spielmodus wählen:")
    print("1. Mensch vs. Mensch")
    print("2. Mensch vs. Computer")
    mode = input("Modus (1/2): ")

    if mode == '1':
        p1_type = 'human'
        p2_type = 'human'
    else:
        print("Wer soll beginnen?")
        print("1. Mensch")
        print("2. Computer")
        first = input("Wähle (1/2): ")
        if first == '1':
            p1_type = 'human'
            p2_type = 'computer'
        else:
            p1_type = 'computer'
            p2_type = 'human'

    board = create_board()
    current_symbol = 'X'
    player_types = {'X': p1_type, 'O': p2_type}

    print_board(board)

    while True:
        player_type = player_types[current_symbol]
        print(f"Spieler {current_symbol} ({'Computer' if player_type == 'computer' else 'Mensch'}) ist am Zug.")

        if player_type == 'human':
            col = get_human_move(board)
        else:
            human_symbol = switch_player(current_symbol)
            col = get_computer_move(board, current_symbol, human_symbol)
            print(f"Computer wählt Spalte {col}")

        move = make_move(board, col, current_symbol)
        if move is None:
            print("Diese Spalte ist voll. Versuch es erneut.")
            continue

        row, col = move
        print_board(board)

        if check_win(board, row, col, current_symbol):
            print(f"Spieler {current_symbol} gewinnt!")
            break

        if is_draw(board):
            print("Unentschieden!")
            break

        current_symbol = switch_player(current_symbol)

def main():
    while True:
     play_game()
     erneut = input("Möchtest du erneut spielen? (j/n): ").strip().lower()
     if erneut != 'j':
      print("Danke fürs Spielen! Auf Wiedersehen.")
     break

if __name__ == "__main__":
    main()

 