import socket
import pickle
import tkinter as tk
from tkinter import messagebox

SIZE = 5
SHIPS = 3
CELL_SIZE = 40

def create_board():
    return [["~"] * SIZE for _ in range(SIZE)]

CELL_COLORS = {
    "~": "lightblue",
    "S": "gray",
    "X": "red",
    "O": "white"
}

class BattleshipClient(tk.Tk):
    def __init__(self, host, port):
        super().__init__()
        self.title("Battleship Client")
        self.resizable(False, False)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.client.setblocking(False)

        self.player_board = create_board()
        self.opponent_board = create_board()

        self.turn = False
        self.ships_placed = 0
        self.placing_ships = True
        self.waiting_for_server_board = False

        self.create_widgets()
        self.status_label.config(text="Place your ships by clicking your board.")

        self.after(100, self.check_for_server_data)

    def create_widgets(self):
        tk.Label(self, text="Your Board").grid(row=0, column=0)
        tk.Label(self, text="Opponent Board").grid(row=0, column=1)

        self.player_frame = tk.Frame(self)
        self.player_frame.grid(row=1, column=0, padx=10, pady=10)

        self.opponent_frame = tk.Frame(self)
        self.opponent_frame.grid(row=1, column=1, padx=10, pady=10)

        self.status_label = tk.Label(self, text="", font=("Arial", 14))
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10)

        self.player_buttons = []
        for i in range(SIZE):
            row_buttons = []
            for j in range(SIZE):
                btn = tk.Button(self.player_frame, width=3, height=1,
                                bg=CELL_COLORS["~"],
                                command=lambda x=i, y=j: self.player_board_click(x, y))
                btn.grid(row=i, column=j)
                row_buttons.append(btn)
            self.player_buttons.append(row_buttons)

        self.opponent_buttons = []
        for i in range(SIZE):
            row_buttons = []
            for j in range(SIZE):
                btn = tk.Button(self.opponent_frame, width=3, height=1,
                                bg=CELL_COLORS["~"],
                                command=lambda x=i, y=j: self.opponent_board_click(x, y))
                btn.grid(row=i, column=j)
                row_buttons.append(btn)
            self.opponent_buttons.append(row_buttons)

        self.update_boards()

    def update_boards(self):
        for i in range(SIZE):
            for j in range(SIZE):
                cell = self.player_board[i][j]
                color = CELL_COLORS.get(cell, "lightblue")
                text = ""
                if cell == "S":
                    text = "🚢"
                elif cell == "X":
                    text = "💥"
                elif cell == "O":
                    text = "⚪"
                state = "normal" if self.placing_ships else "disabled"
                self.player_buttons[i][j].config(bg=color, text=text, state=state)

        for i in range(SIZE):
            for j in range(SIZE):
                cell = self.opponent_board[i][j]
                if cell == "S":
                    color = CELL_COLORS["~"]
                    text = ""
                else:
                    color = CELL_COLORS.get(cell, "lightblue")
                    text = ""
                    if cell == "X":
                        text = "💥"
                    elif cell == "O":
                        text = "⚪"
                state = "normal" if self.turn and not self.placing_ships else "disabled"
                self.opponent_buttons[i][j].config(bg=color, text=text, state=state)

    def player_board_click(self, x, y):
        if not self.placing_ships:
            return
        if self.player_board[x][y] == "~":
            self.player_board[x][y] = "S"
            self.ships_placed += 1
            self.update_boards()

            if self.ships_placed == SHIPS:
                self.placing_ships = False
                self.status_label.config(text="Sending your ships to server...")
                self.update_boards()
                self.client.send(pickle.dumps(self.player_board))
                self.waiting_for_server_board = True

    def opponent_board_click(self, x, y):
        if not self.turn:
            self.status_label.config(text="Not your turn!")
            return
        if self.opponent_board[x][y] in ["X", "O"]:
            self.status_label.config(text="Already targeted that cell!")
            return

        self.client.send(pickle.dumps((x, y)))
        self.status_label.config(text=f"Attacking ({x}, {y})...")
        self.turn = False
        self.update_boards()

    def check_for_server_data(self):
        try:
            data = self.client.recv(4096)
            if data:
                payload = pickle.loads(data)
                # print("Received:", payload)  # Uncomment for debug

                if self.placing_ships and self.waiting_for_server_board:
                    # Receive opponent's board
                    self.opponent_board = payload
                    self.status_label.config(text="Opponent ships received. Waiting for turn...")
                    self.waiting_for_server_board = False
                    self.turn = False  # Server starts first (or implement random start)
                    self.update_boards()

                elif payload == "LOSE":
                    messagebox.showinfo("Game Over", "You lose!")
                    self.status_label.config(text="Game Over. You lose!")
                    self.turn = False
                    self.update_boards()

                elif payload == "WIN":
                    messagebox.showinfo("Game Over", "You win!")
                    self.status_label.config(text="Game Over. You win!")
                    self.turn = False
                    self.update_boards()

                elif isinstance(payload, tuple) and len(payload) == 2:
                    move, hit = payload
                    x, y = move

                    if not self.turn:
                        # Opponent attacked us
                        self.player_board[x][y] = "X" if hit else "O"
                        self.status_label.config(text=f"Opponent attacked ({x},{y}) -> {'Hit' if hit else 'Miss'}")
                        self.turn = True
                    else:
                        # Result of our attack
                        self.opponent_board[x][y] = "X" if hit else "O"
                        self.status_label.config(text=f"Your attack on ({x},{y}) -> {'Hit' if hit else 'Miss'}")
                        self.turn = False

                    self.update_boards()

                else:
                    print("Unknown message:", payload)

        except BlockingIOError:
            pass
        except ConnectionResetError:
            messagebox.showerror("Connection", "Lost connection to server.")
            self.destroy()

        self.after(100, self.check_for_server_data)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5555
    app = BattleshipClient(HOST, PORT)
    app.mainloop()
