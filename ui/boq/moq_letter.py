import tkinter as tk
from datetime import datetime
import os

from ui.boq.pdf_utils import save_letter_as_pdf


def show_moq_letter(parent, boq_data, booking_ref, on_sent_callback=None):
    win = tk.Toplevel(parent)
    win.title("Follow-up (MOQ)")
    win.geometry("520x620")
    win.resizable(False, False)

    # ================= LETTER CONTENT =================
    text = tk.Text(win, wrap="word", font=("Segoe UI", 10))
    text.pack(expand=True, fill="both", padx=10, pady=10)

    letter_text = f"""Minimum Order Quantity (MOQ)

To
{boq_data.get('Buyer Name', '')}

Dear Sir/Madam,

Greetings of the day! Hope you are doing well.

Thanks for your response and for your interest in our product.
Kindly let us know the specifications and details of the products
as per your requirement.

Ref No : {booking_ref}
Date   : {datetime.now().strftime("%d/%m/%Y")}

------------------------------------------------------------
Particulars                     Specifications
------------------------------------------------------------
Product Name                    {boq_data.get('Product Name & Variety', '')}
Product Packing Size & Quantity
Packing Material & Labelling
Required Test & Certificates
Mode of Shipment
INCO Terms
Payment Terms
Final Destination & Date
Remarks                         WAITING FOR REPLY
------------------------------------------------------------

For any further clarifications, please do not hesitate to get back to us.

We are looking forward to your valuable order.

Thanks and with Best Regards,

SINDHU
WCC MSC [REG : 24PDS20]
"""

    text.insert("1.0", letter_text)
    text.config(state="disabled")

    # ================= SEND BUTTON =================
    def send_letter():
        # ---------- SAVE PDF ----------
        pdf_path = save_letter_as_pdf(
            letter_text=letter_text,
            file_name=f"MOQ_Letter_{booking_ref}.pdf",
            sub_folder="moq_letters"
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
