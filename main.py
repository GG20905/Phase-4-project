#To access the project in order to run it Cd into Lib then run python3 main.py

from app import App
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()