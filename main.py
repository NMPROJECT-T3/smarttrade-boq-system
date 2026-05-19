import sys
sys.dont_write_bytecode = True
import tkinter as tk
from ui.login import open_login

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_login(root)
root.mainloop()