import tkinter as tk
from tkinter import messagebox

# Константы
PLAYER = "X"
BOT = "O"


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [["" for _ in range(3)] for _ in range(3)]

        self.create_buttons()

        self.player_turn = True  # Игрок начинает

    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=("Arial", 40), width=5, height=2,
                                command=lambda x=i, y=j: self.player_move(x, y))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def player_move(self, x, y):
        if not self.player_turn:
            return
        if self.board[x][y] == "":
            self.buttons[x][y].config(text=PLAYER, state="disabled")
            self.board[x][y] = PLAYER
            if self.check_winner(self.board, PLAYER):
                messagebox.showinfo("Игра окончена", "Вы выиграли!")
                self.reset()
                return
            elif self.is_draw(self.board):
                messagebox.showinfo("Игра окончена", "Ничья!")
                self.reset()
                return
            else:
                self.player_turn = False
                self.root.after(500, self.bot_move)  # ход бота с небольшой задержкой

    def bot_move(self):
        move = self.find_best_move(self.board)
        if move:
            x, y = move
            self.board[x][y] = BOT
            self.buttons[x][y].config(text=BOT, state="disabled")
            if self.check_winner(self.board, BOT):
                messagebox.showinfo("Игра окончена", "Бот выиграл!")
                self.reset()
                return
            elif self.is_draw(self.board):
                messagebox.showinfo("Игра окончена", "Ничья!")
                self.reset()
                return
        self.player_turn = True

    def check_winner(self, board, player):
        # Проверка строк, столбцов и диагоналей
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
            if all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self, board):
        return all(board[i][j] != "" for i in range(3) for j in range(3))

    def find_best_move(self, board):
        best_val = -float('inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = BOT
                    move_val = self.minimax(board, 0, False)
                    board[i][j] = ""
                    if move_val > best_val:
                        best_val = move_val
                        best_move = (i, j)
        return best_move

    def minimax(self, board, depth, is_max):
        if self.check_winner(board, BOT):
            return 10 - depth
        if self.check_winner(board, PLAYER):
            return depth - 10
        if self.is_draw(board):
            return 0

        if is_max:
            best = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = BOT
                        val = self.minimax(board, depth + 1, False)
                        board[i][j] = ""
                        best = max(best, val)
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = PLAYER
                        val = self.minimax(board, depth + 1, True)
                        board[i][j] = ""
                        best = min(best, val)
            return best

    def reset(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal")
        self.player_turn = True


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()