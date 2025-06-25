import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog
from vier_gewinnt_game import create_board, make_move, is_valid_move, check_win, is_draw, switch_player, get_computer_move

ROWS = 6
COLUMNS = 7

class VierGewinntGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vier Gewinnt")
        self.board = create_board()
        self.current_symbol = 'X'
        self.vs_computer = False
        self.player_types = {'X': 'human', 'O': 'human'}
        self.buttons = []
        self.setup_menu()
        self.create_widgets()
        self.choose_game_mode()
        self.update_board()

    def setup_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Spiel", menu=game_menu)
        game_menu.add_command(label="Neues Spiel (2 Spieler)", command=self.new_game_human)
        game_menu.add_command(label="Neues Spiel (vs Computer)", command=self.new_game_computer)
        game_menu.add_separator()
        game_menu.add_command(label="Beenden", command=self.root.quit)

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.buttons = []
        for col in range(COLUMNS):
            btn = tk.Button(self.frame, text=str(col), width=4, height=2, command=lambda c=col: self.handle_move(c))
            btn.grid(row=0, column=col)
            self.buttons.append(btn)
        # Use Canvas for round slots
        self.canvas = tk.Canvas(self.frame, width=COLUMNS*60, height=ROWS*60, bg='blue', highlightthickness=0)
        self.canvas.grid(row=1, column=0, columnspan=COLUMNS)
        self.canvas_slots = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLUMNS):
                x1 = c*60+5
                y1 = r*60+5
                x2 = x1+50
                y2 = y1+50
                oval = self.canvas.create_oval(x1, y1, x2, y2, fill='white', outline='black', width=2)
                self.canvas_slots[r][c] = oval

    def update_board(self):
        for r in range(ROWS):
            for c in range(COLUMNS):
                symbol = self.board[r][c]
                color = 'white' if symbol == ' ' else ('red' if symbol == 'X' else 'yellow')
                self.canvas.itemconfig(self.canvas_slots[r][c], fill=color)

    def handle_move(self, col):
        if not is_valid_move(self.board, col):
            messagebox.showinfo("Ungültig", "Diese Spalte ist voll.")
            return
        move = make_move(self.board, col, self.current_symbol)
        if move is None:
            return
        row, col = move
        self.update_board()
        if check_win(self.board, row, col, self.current_symbol):
            self.update_board()
            if messagebox.askyesno("Spielende", f"Spieler {self.current_symbol} gewinnt!\nNeues Spiel starten?"):
                self.choose_game_mode()
            else:
                self.root.destroy()
            return
        if is_draw(self.board):
            if messagebox.askyesno("Spielende", "Unentschieden!\nNeues Spiel starten?"):
                self.choose_game_mode()
            else:
                self.root.destroy()
            return
        self.current_symbol = switch_player(self.current_symbol)
        if self.vs_computer and self.player_types[self.current_symbol] == 'computer':
            self.root.after(500, self.computer_move)

    def computer_move(self):
        human_symbol = switch_player(self.current_symbol)
        col = get_computer_move(self.board, self.current_symbol, human_symbol)
        self.handle_move(col)

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state='disabled')

    def enable_buttons(self):
        for btn in self.buttons:
            btn.config(state='normal')

    def choose_game_mode(self):
        mode = tkinter.simpledialog.askstring(
            "Spielmodus wählen",
            "Modus wählen:\n1 = Mensch vs. Mensch\n2 = Mensch vs. Computer",
            parent=self.root
        )
        if mode == '2':
            self.vs_computer = True
            self.player_types = {'X': 'human', 'O': 'computer'}
        else:
            self.vs_computer = False
            self.player_types = {'X': 'human', 'O': 'human'}
        self.board = create_board()
        self.current_symbol = 'X'
        self.update_board()
        self.enable_buttons()

    def new_game_human(self):
        self.choose_game_mode()

    def new_game_computer(self):
        self.vs_computer = True
        self.player_types = {'X': 'human', 'O': 'computer'}
        self.board = create_board()
        self.current_symbol = 'X'
        self.update_board()
        self.enable_buttons()

if __name__ == "__main__":
    root = tk.Tk()
    app = VierGewinntGUI(root)
    root.mainloop()
