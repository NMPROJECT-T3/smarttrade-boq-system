import tkinter as tk
from datetime import datetime
import sqlite3
import os

from ui.boq.pdf_utils import save_letter_as_pdf

# ================= PATH CONFIG =================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DB = os.path.join(BASE_DIR, "database", "boq_system.db")


def show_reminder_letter(parent, booking_ref, reminder_no, on_sent_callback=None):
    win = tk.Toplevel(parent)
    win.title("Reminder Letter")
    win.geometry("520x520")
    win.resizable(False, False)

    text = tk.Text(win, wrap="word", font=("Segoe UI", 10))
    text.pack(expand=True, fill="both", padx=10, pady=10)

    # ================= LETTER CONTENT =================
    letter_text = f"""REMINDER LETTER

Ref No : {booking_ref}
Date   : {datetime.now().strftime("%d/%m/%Y")}

Dear Sir/Madam,

Greetings of the day.

This is a gentle reminder regarding our previous communication.
We are awaiting your response to proceed further with the order
formalities.

Kindly provide your confirmation or required details at the
earliest convenience.

Reminder No : {reminder_no}

Thank you for your attention.

Regards,
Sales Team
"""

    text.insert("1.0", letter_text)
    text.config(state="disabled")

    # ================= SEND BUTTON =================
    def send_letter():
        # ---------- SAVE PDF ----------
        pdf_path = save_letter_as_pdf(
            letter_text=letter_text,
            file_name=f"Reminder_Letter_{booking_ref}_R{reminder_no}.pdf",
            sub_folder="reminder_letters"
        )

        win.destroy()

        # ---------- CALLBACK ----------
        if on_sent_callback:
            on_sent_callback()

        # ---------- AUTO OPEN PDF ----------
        try:
            os.startfile(pdf_path)
        except Exception:
            pass

    tk.Button(
        win,
        text="Send",
        bg="#1f4e79",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=12,
        command=send_letter
    ).pack(pady=10)
