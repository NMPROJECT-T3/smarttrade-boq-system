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


def show_initial_letter(parent, buyer_data, booking_ref, on_sent_callback=None):
    win = tk.Toplevel(parent)
    win.title("Initial Letter")
    win.geometry("520x520")
    win.resizable(False, False)

    text = tk.Text(win, wrap="word", font=("Segoe UI", 10))
    text.pack(expand=True, fill="both", padx=10, pady=10)

    # ================= LETTER CONTENT =================
    letter_text = f"""Dear {buyer_data['Buyer Name']},

Greetings from our organization.

This is with reference to your enquiry received from
{buyer_data['Reference From']}.

We are pleased to initiate our communication regarding
the requested product and will share further details shortly.

Buyer Contact:
{buyer_data['Place, E-Mail ID & Phone #']}

Thank you for your interest.

Regards,
Sales Team
"""

    text.insert("1.0", letter_text)
    text.config(state="disabled")

    # ================= SEND BUTTON =================
    def send_letter():
        # ---------- STORE IN DATABASE ----------
        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
            INSERT OR REPLACE INTO boq_master
            (booking_ref, buyer_name, email, phone,
            country, region, product_name,
            priority, created_date, stage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            booking_ref,
            buyer_data["Buyer Name"],
            "",   # email (can extract later)
            "",   # phone
            "",   # country
            "",   # region
            "",   # product_name
            "Medium",  # default priority
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "INITIAL"
        ))

        conn.commit()
        conn.close()

        # ---------- SAVE PDF ----------
        pdf_path = save_letter_as_pdf(
            letter_text=letter_text,
            file_name=f"Initial_Letter_{booking_ref}.pdf",
            sub_folder="initial_letters"
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
