import tkinter as tk
from tkinter import ttk
import sqlite3
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DB_PATH = os.path.join(BASE_DIR, "database", "boq_system.db")


def get_status(row):
    reminder_count, buyer_responded, moq_sent = row

    if moq_sent == 1:
        return "BOQ Stage"
    elif buyer_responded == 1:
        return "MOQ Stage"
    elif reminder_count > 0:
        return "Reminder Stage"
    else:
        return "Initial Stage"


def open_boq_buyer_master(parent=None):
    win = tk.Toplevel(parent)
    win.title("BOQ Buyer Master View")
    win.geometry("1100x600")
    win.configure(bg="#eef4fb")

    header = tk.Frame(win, bg="#1f4e79", height=60)
    header.pack(fill="x")

    tk.Label(
        header,
        text="BOQ BUYER MASTER – ANALYTICS VIEW",
        bg="#1f4e79",
        fg="white",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=15)

    columns = (
        "Booking Ref",
        "Buyer Name",
        "Contact",
        "Reference From",
        "Reminder Count",
        "Buyer Responded",
        "MOQ Sent",
        "Current Stage"
    )

    tree = ttk.Treeview(win, columns=columns, show="headings")
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130)

    scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.place(relx=0.97, rely=0.15, relheight=0.7)

    # ---------------- FETCH DATA ----------------
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT booking_ref, buyer_name, contact,
               reference_from,
               reminder_count, buyer_responded,
               moq_sent
        FROM boq_reference
    """)

    rows = cur.fetchall()
    conn.close()

    for row in rows:
        status = get_status((row[4], row[5], row[6]))

        tree.insert("", "end", values=(
            row[0], row[1], row[2], row[3],
            row[4], row[5], row[6],
            status
        ))

    tk.Button(
        win,
        text="Close",
        bg="#c0392b",
        fg="white",
        width=20,
        font=("Segoe UI", 10, "bold"),
        command=win.destroy
    ).pack(pady=10)
