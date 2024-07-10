import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.player = "X"
        self.board = [" " for _ in range(9)]
        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.root, text=" ", font=('normal', 40, 'normal'), width=5, height=2,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def on_button_click(self, index):
        if self.board[index] == " " and self.player == "X":
            self.board[index] = self.player
            self.buttons[index].config(text=self.player)

            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.player} wins!")
                self.reset_game()
                return
            elif " " not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.reset_game()
                return
            else:
                self.player = "O"
                self.root.after(500, self.computer_move)

    def computer_move(self):
        move = self.find_best_move()
        self.board[move] = "O"
        self.buttons[move].config(text="O")

        if self.check_winner():
            messagebox.showinfo("Tic Tac Toe", "Player O wins!")
            self.reset_game()
        elif " " not in self.board:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            self.reset_game()
        else:
            self.player = "X"

    def find_best_move(self):
        # Check for a winning move
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                if self.check_winner():
                    self.board[i] = " "
                    return i
                self.board[i] = " "

        # Block opponent's winning move
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "X"
                if self.check_winner():
                    self.board[i] = " "
                    return i
                self.board[i] = " "

        # Choose a random move if no immediate win or block is needed
        for i in range(9):
            if self.board[i] == " ":
                return i

    def check_winner(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != " ":
                return True
        return False

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ")
        self.player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
