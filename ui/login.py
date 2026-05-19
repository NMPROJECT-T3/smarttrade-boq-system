import tkinter as tk
from tkinter import messagebox
from ui.dashboard import open_dashboard

# ================= ENTER KEY NAVIGATION =================
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

def open_login(parent):
    login_win = tk.Toplevel(parent)
    login_win.title("ERP Login")
    login_win.geometry("380x300")
    login_win.resizable(False, False)
    login_win.configure(bg="#f4f6f9")

    # ================= CENTER WINDOW =================
    screen_w = login_win.winfo_screenwidth()
    screen_h = login_win.winfo_screenheight()
    x = (screen_w // 2) - 190
    y = (screen_h // 2) - 150
    login_win.geometry(f"380x300+{x}+{y}")

    # ================= LOGIN LOGIC =================
    def login():
        if entry_user.get() == "admin" and entry_pass.get() == "123":
            login_win.destroy()
            open_dashboard(parent)
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    # ================= HEADER =================
    header = tk.Frame(login_win, bg="#0b5394", height=60)
    header.pack(fill="x")

    tk.Label(
        header,
        text="ERP MANAGEMENT SYSTEM",
        bg="#0b5394",
        fg="white",
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    # ================= FORM =================
    form = tk.Frame(login_win, bg="white", bd=2, relief="groove")
    form.place(x=40, y=90, width=300, height=170)

    # Username
    tk.Label(form, text="Username", bg="white").place(x=30, y=20)
    entry_user = tk.Entry(form, width=28)
    entry_user.place(x=30, y=45)

    # Password
    tk.Label(form, text="Password", bg="white").place(x=30, y=80)
    entry_pass = tk.Entry(form, width=28, show="*")
    entry_pass.place(x=30, y=105)

    # Login Button (CREATE FIRST)
    login_btn = tk.Button(
        form,
        text="LOGIN",
        bg="#0b5394",
        fg="white",
        font=("Arial", 10, "bold"),
        width=20,
        command=login
    )
    login_btn.place(x=55, y=135)

    # ================= KEY BINDINGS =================
    entry_user.bind("<Return>", focus_next_widget)
    entry_pass.bind("<Return>", lambda e: login_btn.invoke())

    # Autofocus
    entry_user.focus_set()
