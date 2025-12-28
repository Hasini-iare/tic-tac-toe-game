import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Tic Tac Toe")

board = [" " for _ in range(9)]
buttons = []

HUMAN = "X"
AI = "O"

def check_winner(player):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    return any(board[a] == board[b] == board[c] == player for a,b,c in wins)

def is_draw():
    return " " not in board

def minimax(is_maximizing):
    if check_winner(AI):
        return 1
    if check_winner(HUMAN):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = -100
        for i in range(9):
            if board[i] == " ":
                board[i] = AI
                score = minimax(False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = 100
        for i in range(9):
            if board[i] == " ":
                board[i] = HUMAN
                score = minimax(True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -100
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = AI
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i

    board[move] = AI
    buttons[move].config(text=AI)

    if check_winner(AI):
        messagebox.showinfo("Game Over", "I win!")
        reset()
    elif is_draw():
        messagebox.showinfo("Game Over", "Draw!")
        reset()

def click(i):
    if board[i] != " ":
        return

    board[i] = HUMAN
    buttons[i].config(text=HUMAN)

    if check_winner(HUMAN):
        messagebox.showinfo("Game Over", "You win!")
        reset()
        return
    elif is_draw():
        messagebox.showinfo("Game Over", "Draw!")
        reset()
        return

    root.after(300, ai_move)

def reset():
    for i in range(9):
        board[i] = " "
        buttons[i].config(text="")

for i in range(9):
    btn = tk.Button(
        root,
        text="",
        font=("Arial", 24),
        width=5,
        height=2,
        command=lambda i=i: click(i)
    )
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

root.mainloop()

