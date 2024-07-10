import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.player = "X"
        self.board = [" " for _ in range(9)]
        self.buttons = []
        self.create_ui()

    def create_ui(self):
        # Create frames
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)
        
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        # Create the board
        self.create_board()

        # Create the reset button
        self.create_reset_button()

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.board_frame, text=" ", font=('Arial', 36, 'bold'), width=5, height=2,
                               bg='#f0f0f0', activebackground='#d0d0d0', relief='raised', 
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

    def create_reset_button(self):
        reset_button = tk.Button(self.control_frame, text="Reset Game", font=('Arial', 16), bg='#ff6666', fg='white',
                                 command=self.reset_game, relief='raised')
        reset_button.pack(pady=10)

    def on_button_click(self, index):
        if self.board[index] == " " and self.player == "X":
            self.board[index] = self.player
            self.buttons[index].config(text=self.player, fg='#000000')

            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.player} wins!")
                self.highlight_winner()
                return
            elif " " not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                return
            else:
                self.player = "O"
                self.root.after(500, self.computer_move)

    def computer_move(self):
        move = self.find_best_move()
        self.board[move] = "O"
        self.buttons[move].config(text="O", fg='#ff0000')

        if self.check_winner():
            messagebox.showinfo("Tic Tac Toe", "Player O wins!")
            self.highlight_winner()
        elif " " not in self.board:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
        else:
            self.player = "X"

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
        self.player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
