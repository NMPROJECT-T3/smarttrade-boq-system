import tkinter as tk
from datetime import datetime
import sqlite3
import os

# ================= DATABASE CONFIG =================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
DB_PATH = os.path.join(BASE_DIR, "database", "boq_system.db")


def show_boq_confirmation_letter(parent, boq_data, booking_ref, on_sent_callback=None):

    win = tk.Toplevel(parent)
    win.title("BOQ Confirmation")
    win.geometry("750x800")
    win.resizable(False, False)

    # ================= TEXT AREA =================
    text = tk.Text(win, wrap="word", font=("Segoe UI", 10))
    text.pack(expand=True, fill="both", padx=10, pady=10)

    letter = f"""Bill Of Quantity (BOQ)

To
{boq_data.get('Buyer Name', '')}

Dear Sir/Madam,

Subject: Confirmation review on Product Specification details – Reg.

Greetings of the day.

Thank you for your confirmation. The product specifications are listed below for your review:

Ref No : {booking_ref}
Date   : {datetime.now().strftime("%d/%m/%Y")}

------------------------------------------------------------
Particulars                         Specifications
------------------------------------------------------------
Product Name                        {boq_data.get('Product Name & Variety', '')}
Product Packing Size & Quantity     {boq_data.get('Product Packing Size & Qty', '')}
Packing Material & Labelling        {boq_data.get('Packing Material & Labelling', '')}
Required Test & Certificates        {boq_data.get('Required Test & Certificates', '')}
Mode of Shipment                    {boq_data.get('Mode of Shipment', '')}
INCO Terms                          {boq_data.get('INCO Terms', '')}
Payment Terms                       {boq_data.get('Payment Terms', '')}
Final Destination & Date            {boq_data.get('Final Destination & Date', '')}
------------------------------------------------------------

Shipment Status : CONFIRMED

We will proceed with Proforma Invoice and shipment scheduling.

Regards,
Sales Team
"""

    text.insert("1.0", letter)
    text.config(state="disabled")

    # ================= SEND BUTTON =================
    def confirm_and_close():

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
            UPDATE boq_reference
            SET buyer_responded = 1,
                moq_sent = 1
            WHERE booking_ref = ?
        """, (booking_ref,))

        conn.commit()
        conn.close()

        win.destroy()

        if on_sent_callback:
            on_sent_callback()

    tk.Button(
        win,
        text="Send & Confirm",
        bg="#1f4e79",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        width=18,
        height=2,
        command=confirm_and_close
    ).pack(pady=15)
