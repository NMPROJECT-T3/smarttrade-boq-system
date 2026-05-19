import tkinter as tk
from datetime import datetime, date
from tkinter import messagebox
from ui.boq.letters import show_initial_letter
from ui.boq.reminder_letter import show_reminder_letter
from ui.boq.moq_letter import show_moq_letter
from ui.boq.boq_confirmation_letter import show_boq_confirmation_letter
import sqlite3
import os


def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"


# ================= DATABASE CONFIG =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "database", "boq_system.db")


# ================= DB HELPERS =================
def get_buyer_by_booking_ref(booking_ref):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT buyer_name, contact, reference_from,
               reminder_count, buyer_responded,
               moq_sent, moq_product,
               country, region
        FROM boq_reference
        WHERE booking_ref = ?
    """, (booking_ref,))

    row = cur.fetchone()
    conn.close()
    return row


def increment_reminder_count(booking_ref):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE boq_reference
        SET reminder_count = reminder_count + 1
        WHERE booking_ref = ?
    """, (booking_ref,))
    conn.commit()
    conn.close()


def mark_buyer_responded(booking_ref):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE boq_reference
        SET buyer_responded = 1
        WHERE booking_ref = ?
    """, (booking_ref,))
    conn.commit()
    conn.close()


def store_moq_details(booking_ref, product_name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE boq_reference
        SET moq_sent = 1,
            moq_date = ?,
            moq_product = ?
        WHERE booking_ref = ?
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        product_name,
        booking_ref
    ))
    conn.commit()
    conn.close()


# ================= MAIN FORM =================
def open_boq_form(parent=None):

    win = tk.Toplevel(parent) if parent else tk.Tk()
    win.title("Business Communication Procedure (BOQ)")
    win.geometry("1200x700")
    win.configure(bg="#eef4fb")
    win.resizable(False, False)

    # ================= HEADER =================
    header = tk.Frame(win, bg="#1f4e79", height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Business Communication Procedure (Bill Of Quantity - BOQ)",
        bg="#1f4e79",
        fg="white",
        font=("Segoe UI", 14, "bold")
    ).place(x=20, y=18)

    body = tk.Frame(win, bg="#eef4fb")
    body.place(x=0, y=70, relwidth=1, relheight=1)

    form = tk.Frame(body, bg="#eef4fb")
    form.place(x=20, y=20, width=880, height=620)

    labels = [
        "Date", "Booking Ref #", "Buyer Name",
        "Country", "Region",
        "Place, E-Mail ID & Phone #", "Reference From",
        "Product Name & Variety",
        "Product Packing Size & Qty",
        "Packing Material & Labelling",
        "Required Test & Certificates",
        "Mode of Shipment", "INCO Terms",
        "Payment Terms",
        "Final Destination & Date"
    ]

    entries = {}
    y = 10

    for lbl in labels:
        tk.Label(
            form,
            text=lbl,
            bg="#eef4fb",
            fg="#1f4e79",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).place(x=10, y=y, width=260)

        entry = tk.Entry(form, width=65, state="disabled")
        entry.place(x=280, y=y)
        entry.bind("<Return>", focus_next_widget)
        entries[lbl] = entry
        y += 35

    # Auto Date
    entries["Date"].config(state="normal")
    entries["Date"].insert(0, date.today().strftime("%d/%m/%Y"))
    entries["Date"].config(state="readonly")

    entries["Booking Ref #"].config(state="normal")

    # ================= ACTION PANEL =================
    action = tk.Frame(body, bg="#eef4fb")
    action.place(x=920, y=20, width=250, height=620)

    def action_button(text):
        return tk.Button(
            action,
            text=text,
            width=22,
            height=2,
            bg="white",
            fg="#1f4e79",
            font=("Segoe UI", 10, "bold"),
            relief="solid",
            bd=1,
            state="disabled"
        )

    initial_letter_btn = action_button("Initial Letter")
    reminder_btn = action_button("Reminder Letter")
    moq_btn = action_button("Follow-up (MOQ)")
    confirm_btn = action_button("Confirmation (BOQ)")

    initial_letter_btn.pack(pady=12)
    reminder_btn.pack(pady=12)
    moq_btn.pack(pady=12)
    confirm_btn.pack(pady=12)

    # ================= FLOW CONTROL =================
    def lock_all_specs():
        for f in labels[7:]:
            entries[f].config(state="disabled")

    def unlock_moq_only():
        entries["Product Name & Variety"].config(state="normal")

    def unlock_boq_specs():
        for f in labels[8:]:
            entries[f].config(state="normal")

    lock_all_specs()

    # ================= BOOKING FLOW =================
    def booking_ref_popup(event=None):

        ref = entries["Booking Ref #"].get().strip()
        if not ref:
            return

        record = get_buyer_by_booking_ref(ref)

        if not record:
            if messagebox.askyesno("New Reference", "New Booking Reference?"):
                for f in ["Buyer Name","Country","Region",
                          "Place, E-Mail ID & Phone #","Reference From"]:
                    entries[f].config(state="normal")
                initial_letter_btn.config(state="normal")
            return

        buyer, contact, ref_from, reminder_count, responded, moq_sent, moq_product, country, region = record

        for f in ["Buyer Name","Country","Region",
                  "Place, E-Mail ID & Phone #","Reference From"]:
            entries[f].config(state="normal")

        entries["Buyer Name"].delete(0, tk.END)
        entries["Buyer Name"].insert(0, buyer)

        entries["Country"].delete(0, tk.END)
        entries["Country"].insert(0, country or "")

        entries["Region"].delete(0, tk.END)
        entries["Region"].insert(0, region or "")

        entries["Place, E-Mail ID & Phone #"].delete(0, tk.END)
        entries["Place, E-Mail ID & Phone #"].insert(0, contact)

        entries["Reference From"].delete(0, tk.END)
        entries["Reference From"].insert(0, ref_from)

        for f in ["Buyer Name","Country","Region",
                  "Place, E-Mail ID & Phone #","Reference From"]:
            entries[f].config(state="readonly")

        initial_letter_btn.config(state="disabled")

        if responded == 0:
            if messagebox.askyesno("Buyer Response",
                                   "Have you received a response from the buyer?"):
                mark_buyer_responded(ref)
                responded = 1

        if responded == 1 and moq_sent == 1:
            entries["Product Name & Variety"].config(state="normal")
            entries["Product Name & Variety"].delete(0, tk.END)
            entries["Product Name & Variety"].insert(0, moq_product)
            entries["Product Name & Variety"].config(state="readonly")

            unlock_boq_specs()
            confirm_btn.config(state="normal")
            moq_btn.config(state="disabled")
            reminder_btn.config(state="disabled")
            return

        if responded == 1:
            moq_btn.config(state="normal")
            reminder_btn.config(state="disabled")
            unlock_moq_only()
        else:
            moq_btn.config(state="disabled")
            if reminder_count < 3:
                reminder_btn.config(state="normal")
            else:
                reminder_btn.config(state="disabled")

    entries["Booking Ref #"].bind("<Return>", booking_ref_popup)

    # ================= BUTTON ACTIONS =================
    def generate_initial_letter():

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
            INSERT OR REPLACE INTO boq_reference
            (booking_ref,buyer_name,contact,reference_from,
             country,region,created_date)
            VALUES (?,?,?,?,?,?,?)
        """,(
            entries["Booking Ref #"].get(),
            entries["Buyer Name"].get(),
            entries["Place, E-Mail ID & Phone #"].get(),
            entries["Reference From"].get(),
            entries["Country"].get(),
            entries["Region"].get(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        show_initial_letter(
            win,
            {
                "Buyer Name": entries["Buyer Name"].get(),
                "Place, E-Mail ID & Phone #": entries["Place, E-Mail ID & Phone #"].get(),
                "Reference From": entries["Reference From"].get()
            },
            entries["Booking Ref #"].get(),
            on_sent_callback=win.destroy
        )

    initial_letter_btn.config(command=generate_initial_letter)

    def send_reminder():
        ref = entries["Booking Ref #"].get()
        increment_reminder_count(ref)

        show_reminder_letter(
            win,
            ref,
            None,
            on_sent_callback=win.destroy
        )

    reminder_btn.config(command=send_reminder)

    def send_moq():
        ref = entries["Booking Ref #"].get()
        product = entries["Product Name & Variety"].get()

        store_moq_details(ref, product)

        show_moq_letter(
            win,
            {
                "Buyer Name": entries["Buyer Name"].get(),
                "Product Name & Variety": product
            },
            ref,
            on_sent_callback=win.destroy
        )

    moq_btn.config(command=send_moq)

    confirm_btn.config(command=lambda:
        show_boq_confirmation_letter(
            win,
            {k: entries[k].get() for k in labels[2:]},
            entries["Booking Ref #"].get(),
            on_sent_callback=win.destroy))

    tk.Button(
        action,
        text="Exit",
        width=22,
        height=2,
        bg="#c0392b",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        command=win.destroy
    ).pack(side="bottom", pady=30)
