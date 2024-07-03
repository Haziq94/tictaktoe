import tkinter as tk
import random
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
            button = tk.Button(self.root, text=" ", font=('normal',40,'normal'),width=5, height=2,command=lambda i=i:self.on_button_click(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

    def on_button_click(self, index):
        if self.board[index] == " " and self.player == "X":
            self.board[index] = self.player
            self.buttons[index].config(text=self.player)
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe",f"Player{self.player} wins!")
                self.reset_games()
                return
            elif " " not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.reset_games()
                return
            else:
                self.player = "O"
                self.computer_move()

    def computer_move(self):
        '''empty_cells = [i for i in range(9) if self.board[i] == " "]
        index = random.choice(empty_cells)
        self.board[index] = self.player
        self.buttons[index].config(text = self.player)'''

        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.player
                score = self.minimax(self.board,0,False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i
        self.board[best_move] = self.player
        self.buttons[best_move].config(text = self.player)

        if self.check_winner():
            messagebox.showinfo("Tic Tac Toe", f"Player {self.player} wins!")
            self.reset_games()
        elif " " not in self.board:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
        else:
            self.player = "X"

    def minimax(self,board,depth,is_maximizing):
        if self.check_winner():
            return 1 if self.player == "O" else -1
        elif " " not in board:
            return 0 

        if is_maximizing :
            best_score = -float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board,depth+1, False)
                    board[i] = " "
                    best_score = max(score,best_score)
            return best_score
        else:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = score = self.minimax(board,depth+1, True)
                    board[i] = " "
                    best_score = max(score,best_score)
            return best_score

    def check_winner(self):
        win_conditions = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != " " :
                return True
        return False

    def reset_games(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ")
        self.player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
