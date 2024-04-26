import tkinter as tk
import subprocess
from tkinter.messagebox import showinfo

def solve_game():
    output = subprocess.run(["c-solver.exe"], capture_output=True)
    if output.stdout.decode("utf-8") == "Nothing found\r\n":
        showinfo("Info", "This game of solitaire is unwinnable")
    else:
        output = subprocess.run(["main.exe"], capture_output=True)

def deal_new():
    output = subprocess.run(["main.exe", "deal"], capture_output=True)
r = tk.Tk()
r.title('Solitaire Solver')
button = tk.Button(r, text='Solve Solitaire', width=100, command=solve_game)
button2 = tk.Button(r, text='Deal New Game', width=100, command=solve_game)
button.pack()
button2.pack()

r.mainloop()