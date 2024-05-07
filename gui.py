import tkinter as tk
import subprocess
from tkinter.messagebox import showinfo
from tkinter import ttk

def solve_game():
    output = subprocess.run(["c-solver.exe"], capture_output=True)
    if output.stdout.decode("utf-8") == "Nothing found\r\n":
        showinfo("Info", "This game of solitaire is unwinnable")
    else:
        output = subprocess.run(["main.exe"], capture_output=True)

def deal_new():
    output = subprocess.run(["main.exe", "deal"], capture_output=True)

subprocess.Popen(["cracked_solitaire.exe"])
r = tk.Tk()
r.title('Solitaire Solver')

style = ttk.Style()

# Configure the style for the buttons
style.configure('TButton', foreground='black', bg='white', font=('Helvetica', 12))

button = ttk.Button(r, text='Solve Solitaire', width=65, command=solve_game)
button2 = ttk.Button(r, text='Deal New Game', width=65, command=deal_new)
button.pack(pady=25)
button2.pack(pady=10)

r.mainloop()