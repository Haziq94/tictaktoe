import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = [" " for _ in range(9)]
        self.buttons = []
        self.game_mode = "PVP"  # Default to Player vs Player
        self.player = "X"  # Starting player
        self.create_ui()

    def create_ui(self):
        # Create frames
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        # Create the board
        self.create_board()

        # Create the control panel
        self.create_control_panel()

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.board_frame, text=" ", font=('Arial', 36, 'bold'), width=5, height=2,
                               bg='#f0f0f0', activebackground='#d0d0d0', relief='raised',
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

    def create_control_panel(self):
        self.mode_var = tk.StringVar(value=self.game_mode)

        tk.Label(self.control_frame, text="Select Game Mode:", font=('Arial', 14)).pack(pady=5)
        modes = [("Player vs Player", "PVP"), ("Player vs AI", "PVA"), ("AI vs AI", "AIA")]
        for text, mode in modes:
            tk.Radiobutton(self.control_frame, text=text, variable=self.mode_var, value=mode, 
                           font=('Arial', 12), command=self.set_game_mode).pack(anchor=tk.W)

        self.reset_button = tk.Button(self.control_frame, text="Reset Game", font=('Arial', 16), bg='#ff6666', fg='white',
                                     command=self.reset_game, relief='raised')
        self.reset_button.pack(pady=10)

    def set_game_mode(self):
        self.game_mode = self.mode_var.get()
        self.reset_game()

    def on_button_click(self, index):
        if self.board[index] == " " and (self.game_mode in ["PVP", "PVA"] or self.player == "X"):
            self.board[index] = self.player
            self.buttons[index].config(text=self.player, fg='#000000' if self.player == "X" else '#ff0000')

            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.player} wins!")
                self.highlight_winner()
                return
            elif " " not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                return

            if self.game_mode == "PVP":
                self.player = "O" if self.player == "X" else "X"
            elif self.game_mode == "PVA":
                self.player = "O"
                self.root.after(500, self.computer_move)
            elif self.game_mode == "AIA":
                self.player = "O" if self.player == "X" else "X"
                self.root.after(500, self.ai_move)

    def computer_move(self):
        move = self.find_best_move()
        self.board[move] = "O"
        self.buttons[move].config(text="O", fg='#ff0000')

        if self.check_winner():
            messagebox.showinfo("Tic Tac Toe", "AI Player O wins!")
            self.highlight_winner()
        elif " " not in self.board:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
        else:
            self.player = "X"

    def ai_move(self):
        move = self.find_best_move()
        self.board[move] = self.player
        self.buttons[move].config(text=self.player, fg='#ff0000' if self.player == "O" else '#000000')

        if self.check_winner():
            messagebox.showinfo("Tic Tac Toe", f"AI Player {self.player} wins!")
            self.highlight_winner()
        elif " " not in self.board:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
        else:
            # Alternate player
            self.player = "X" if self.player == "O" else "O"
            # Schedule the next move
            self.root.after(500, self.ai_move)

    def find_best_move(self):
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                if self.check_winner():
                    self.board[i] = " "
                    return i
                self.board[i] = " "

        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "X"
                if self.check_winner():
                    self.board[i] = " "
                    return i
                self.board[i] = " "

        for i in range(9):
            if self.board[i] == " ":
                return i

    def check_winner(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != " ":
                return condition
        return False

    def highlight_winner(self):
        winning_condition = self.check_winner()
        if winning_condition:
            for index in winning_condition:
                self.buttons[index].config(bg='lightgreen', fg='black')

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ", bg='#f0f0f0', fg='#000000')
        self.player = "X"  # Start with 'X'
        if self.game_mode == "AIA":
            self.root.after(500, self.ai_move)  # Start AI vs AI with 'X'

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
