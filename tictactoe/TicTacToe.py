import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = [" " for _ in range(9)]
        self.buttons = []
        self.game_mode = "PVP"  # Default to Player vs Player
        self.difficulty = "Easy"  # Default AI difficulty
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
        # Create left and right frames for control panel
        self.left_control_frame = tk.Frame(self.control_frame)
        self.left_control_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)

        self.right_control_frame = tk.Frame(self.control_frame)
        self.right_control_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

        # Game Mode Options
        tk.Label(self.left_control_frame, text="Select Game Mode:", font=('Arial', 14)).pack(pady=5)
        self.mode_var = tk.StringVar(value=self.game_mode)
        modes = [("Player vs Player", "PVP"), ("Player vs AI", "PVA")]
        for text, mode in modes:
            tk.Radiobutton(self.left_control_frame, text=text, variable=self.mode_var, value=mode,
                           font=('Arial', 12), command=self.set_game_mode).pack(anchor=tk.W)

        # Difficulty Options (initially hidden)
        self.difficulty_frame = tk.Frame(self.right_control_frame)
        tk.Label(self.difficulty_frame, text="Select AI Difficulty:", font=('Arial', 14)).pack(pady=5)
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        difficulties = [("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")]
        for text, level in difficulties:
            tk.Radiobutton(self.difficulty_frame, text=text, variable=self.difficulty_var, value=level,
                           font=('Arial', 12), command=self.set_difficulty).pack(anchor=tk.W)
        self.difficulty_frame.pack_forget()  # Hide difficulty options initially

        # Create a frame for the Reset button to ensure it's at the bottom and centered
        self.reset_button_frame = tk.Frame(self.right_control_frame)
        self.reset_button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Reset Button
        self.reset_button = tk.Button(self.reset_button_frame, text="Reset Game", font=('Arial', 16), bg='#ff6666', fg='white',
                                     command=self.reset_game, relief='raised')
        self.reset_button.pack(pady=10, padx=10)

    def set_game_mode(self):
        self.game_mode = self.mode_var.get()
        if self.game_mode == "PVA":
            self.difficulty_frame.pack(side=tk.RIGHT, padx=10)  # Show difficulty options
        else:
            self.difficulty_frame.pack_forget()  # Hide difficulty options
        self.reset_game()

    def set_difficulty(self):
        self.difficulty = self.difficulty_var.get()

    def on_button_click(self, index):
        if self.board[index] == " " and (self.game_mode == "PVP" or (self.game_mode == "PVA" and self.player == "X")):
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
                if self.player == "X":
                    self.player = "O"
                    self.root.after(500, self.computer_move)

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

    def find_best_move(self):
        if self.difficulty == "Easy":
            return self.random_move()
        elif self.difficulty == "Medium":
            return self.medium_move()
        elif self.difficulty == "Hard":
            return self.minimax()

    def random_move(self):
        available_moves = [i for i, spot in enumerate(self.board) if spot == " "]
        return random.choice(available_moves)

    def medium_move(self):
        # Block opponent's winning move or make a winning move
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

        return self.random_move()

    def minimax(self):
        def evaluate(board):
            winner = self.check_winner()
            if winner:
                return 10 if self.player == "O" else -10
            return 0

        def minimax(board, depth, is_max):
            score = evaluate(board)
            if score == 10:
                return score - depth
            if score == -10:
                return score + depth
            if " " not in board:
                return 0

            if is_max:
                best = -float('inf')
                for i in range(9):
                    if board[i] == " ":
                        board[i] = "O"
                        best = max(best, minimax(board, depth + 1, not is_max))
                        board[i] = " "
                return best
            else:
                best = float('inf')
                for i in range(9):
                    if board[i] == " ":
                        board[i] = "X"
                        best = min(best, minimax(board, depth + 1, not is_max))
                        board[i] = " "
                return best

        best_move = -1
        best_val = -float('inf')
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                move_val = minimax(self.board, 0, False)
                self.board[i] = " "
                if move_val > best_val:
                    best_move = i
                    best_val = move_val
        return best_move

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

        if self.game_mode == "PVA" and self.player == "O":
            # Schedule the first AI move if in Player vs AI mode
            self.root.after(500, self.computer_move)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
