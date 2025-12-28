import tkinter as tk
from tkinter import messagebox
import random
import time
import os

number = 0
attempts = 0
start_time = 0
difficulty_range = 100
scores_file = "number_guessing_scores.txt"
scores = {"Easy": None, "Medium": None, "Hard": None}
guess_history_list = []

if os.path.exists(scores_file):
    with open(scores_file, "r") as f:
        for line in f:
            diff, attempt, elapsed = line.strip().split(",")
            scores[diff] = (int(attempt), float(elapsed))

def start_game():
    global number, attempts, start_time, difficulty_range, guess_history_list
    diff = difficulty_var.get()
    if diff == "Easy":
        difficulty_range = 50
    elif diff == "Medium":
        difficulty_range = 100
    else:
        difficulty_range = 500
    number = random.randint(1, difficulty_range)
    attempts = 0
    start_time = time.time()
    guess_history_list = []
    update_scoreboard()
    result_text.set(f"Guess a number between 1 and {difficulty_range}")
    guess_history_text.set("Your guesses: []")
    entry.delete(0, tk.END)
    entry.config(bg="white")

def check_guess():
    global attempts
    guess = entry.get()
    if not guess.isdigit():
        messagebox.showwarning("Invalid Input", "Please enter a valid number.")
        return
    guess_int = int(guess)
    attempts += 1
    guess_history_list.append(guess_int)
    guess_history_text.set(f"Your guesses: {guess_history_list}")
    diff_abs = abs(number - guess_int)
    if diff_abs == 0:
        color = "green"
        feedback = "Correct!"
    elif diff_abs <= 5:
        color = "yellow"
        feedback = "Very close!"
    elif diff_abs > 20:
        color = "lightblue"
        feedback = "Cold"
    else:
        color = "orange"
        feedback = "Warm"
    entry.config(bg=color)
    if guess_int < number:
        result_text.set(f"{feedback} Too low!")
    elif guess_int > number:
        result_text.set(f"{feedback} Too high!")
    else:
        elapsed = round(time.time() - start_time, 2)
        result_text.set(f"Correct! Attempts: {attempts}, Time: {elapsed}s")
        update_scoreboard(attempts, elapsed)
        messagebox.showinfo("Congratulations!", f"You guessed it in {attempts} attempts and {elapsed} seconds!")
        save_scores()
        start_game()

def update_scoreboard(attempts_taken=None, elapsed_time=None):
    diff = difficulty_var.get()
    if attempts_taken:
        current_score = scores[diff]
        if current_score is None or attempts_taken < current_score[0]:
            scores[diff] = (attempts_taken, elapsed_time)
    scoreboard_text.set(
        f"Scores (Least Attempts):\n"
        f"Easy: {scores['Easy'][0] if scores['Easy'] else '-'}\n"
        f"Medium: {scores['Medium'][0] if scores['Medium'] else '-'}\n"
        f"Hard: {scores['Hard'][0] if scores['Hard'] else '-'}"
    )

def save_scores():
    with open(scores_file, "w") as f:
        for diff, val in scores.items():
            if val:
                f.write(f"{diff},{val[0]},{val[1]}\n")

root = tk.Tk()
root.title("Number Guessing Game")

result_text = tk.StringVar(value="Select difficulty and start guessing!")
scoreboard_text = tk.StringVar()
guess_history_text = tk.StringVar(value="Your guesses: []")

tk.Label(root, textvariable=result_text, font=("Arial", 14)).pack(pady=10)

difficulty_var = tk.StringVar(value="Medium")
diff_frame = tk.Frame(root)
diff_frame.pack(pady=5)

for diff in ["Easy", "Medium", "Hard"]:
    tk.Radiobutton(diff_frame, text=diff, variable=difficulty_var, value=diff, font=("Arial", 12), command=start_game).pack(side=tk.LEFT, padx=5)

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=5)

tk.Button(root, text="Guess", font=("Arial", 12), command=check_guess).pack(pady=5)
tk.Button(root, text="Start / Restart", font=("Arial", 12), command=start_game).pack(pady=5)

tk.Label(root, textvariable=guess_history_text, font=("Arial", 12)).pack(pady=5)
tk.Label(root, textvariable=scoreboard_text, font=("Arial", 12), justify="left").pack(pady=10)

start_game()
root.mainloop()

