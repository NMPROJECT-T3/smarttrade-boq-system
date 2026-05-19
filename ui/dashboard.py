import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import os
import subprocess
from ui.boq.boq_form import open_boq_form
from ui.boq.boq_buyer_master_view import open_boq_buyer_master

# ✅ FIXED IMPORT

def open_dashboard(parent=None):
    root = tk.Toplevel(parent) if parent else tk.Tk()
    root.title("ERP Dashboard")
    #root.geometry("1200x600")
    root.state("zoomed")
    root.configure(bg="#eef4fb")

    header = tk.Frame(root, bg="#1f4e79", height=75)
    header.pack(fill="x")

    tk.Label(
        header,
        text="ERP MANAGEMENT SYSTEM",
        bg="#1f4e79",
        fg="white",
        font=("Segoe UI", 16, "bold")
    ).place(x=20, y=12)

    tk.Label(
        header,
        text="SINDHU WCC MSC | REG : 24PDS20",
        bg="#1f4e79",
        fg="#dce6f1",
        font=("Segoe UI", 10)
    ).place(x=22, y=42)

    time_label = tk.Label(header, bg="#1f4e79", fg="white")
    time_label.place(relx=0.82, rely=0.35)

    def update_time():
        time_label.config(
            text=datetime.now().strftime("%A  %d-%m-%Y   %H:%M:%S")
        )
        time_label.after(1000, update_time)

    update_time()

    main = tk.Frame(root, bg="#eef4fb")
    main.pack(fill="both", expand=True, pady=40)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    icons = {
        "Data Input": "data.png",
        "Global Trade": "trade.png",
        "Reports": "report.png",
        "Progress": "progress.png",
        "Settings": "setting.png",
        "Modify": "modify.png"
    }

    for i in range(len(icons)):
        main.columnconfigure(i, weight=1)

    def create_card(col, text, img_name):
        card = tk.Canvas(
            main,
            width=170,
            height=190,
            bg="#eef4fb",
            highlightthickness=0
        )

        card.grid(row=0, column=col, padx=10, pady=20, sticky="n")

        card.create_rectangle(
            10, 10, 160, 180,
            outline="#1f4e79",
            width=2,
            fill="white"
        )

        img_path = os.path.join(BASE_DIR, "assets", img_name)
        img = Image.open(img_path).resize((65, 65))
        icon = ImageTk.PhotoImage(img)
        card.image = icon

        card.create_image(85, 60, image=icon)
        card.create_text(
            85, 135,
            text=text,
            fill="#1f4e79",
            font=("Segoe UI", 10, "bold")
        )

        if text == "Data Input":
            card.bind("<Button-1>", lambda e: open_data_input(
                e.widget.winfo_rootx(),
                e.widget.winfo_rooty() + 200
            ))

        elif text == "Reports":
            card.bind("<Button-1>", lambda e: open_reports(
                e.widget.winfo_rootx(),
                e.widget.winfo_rooty() + 200
            ))

        elif text == "Progress":
            card.bind("<Button-1>", lambda e: open_progress(
                e.widget.winfo_rootx(),
                e.widget.winfo_rooty() + 200
            ))

        elif text == "Settings":
            card.bind("<Button-1>", lambda e: open_settings(
                e.widget.winfo_rootx(),
                e.widget.winfo_rooty() + 200
            ))

        elif text == "Global Trade":
            card.bind("<Button-1>", lambda e: open_global_trade(
                e.widget.winfo_rootx(),
                e.widget.winfo_rooty() + 200
            ))

    for index, (name, img) in enumerate(icons.items()):
        create_card(index, name, img)

    root.mainloop()

def open_data_input(x, y):
    win = tk.Toplevel()
    win.title("Data Input")
    win.geometry("320x360")
    win.configure(bg="#f4f8fb")
    win.resizable(False, False)
    win.geometry(f"+{x}+{y}")

    body = tk.Frame(win, bg="#f4f8fb")
    body.pack(fill="both", expand=True, pady=10)

    options = [
        "Financial Accounting System",
        "Inward Invoice (Purchase)",
        "Outward Invoice (Sales)",
        "Human Resource Management",
        "Customer Information (CRM)",
        "Task Reminder Planning"
    ]

    for opt in options:
        tk.Button(
            body, text=opt, width=32, height=2,
            bg="white", fg="#1f4e79",
            font=("Segoe UI", 10, "bold"),
            relief="solid", bd=1
        ).pack(pady=6)

    tk.Button(
        body, text="Close",
        bg="#c0392b", fg="white",
        width=20, font=("Segoe UI", 10, "bold"),
        command=win.destroy
    ).pack(pady=10)


def open_global_trade(x, y):
    win = tk.Toplevel()
    win.title("Global Trade")
    win.geometry("330x380")
    win.configure(bg="#f4f8fb")
    win.resizable(False, False)
    win.geometry(f"+{x}+{y}")

    frame = tk.Frame(win, bg="#f4f8fb")
    frame.pack(fill="both", expand=True, pady=10)

    options = [
        "Market - Buyer Research",
        "Order Processing",
        "Costing Process",
        "Payment Process",
        "Pre - Shipment Process",
        "Post - Shipment Process",
        "Service Export Process",
        "Reporting Process",
        "Order Tracking Process"
    ]

    for opt in options:
        if opt == "Order Processing":
            tk.Button(
                frame, text=opt, width=32, height=2,
                bg="white", fg="#1f4e79",
                font=("Segoe UI", 10, "bold"),
                relief="solid", bd=1,
                command=lambda: open_order_process(
                    win.winfo_rootx() + 300,
                    win.winfo_rooty() + 80
                )
            ).pack(pady=4)
        else:
            tk.Button(
                frame, text=opt, width=32, height=2,
                bg="white", fg="#1f4e79",
                font=("Segoe UI", 10, "bold"),
                relief="solid", bd=1
            ).pack(pady=4)

    tk.Button(frame, text="Exit", bg="#c0392b", fg="white",
              width=20, command=win.destroy).pack(pady=10)

# ================= ORDER PROCESS (FIXED) =================
def open_order_process(x, y):
    win = tk.Toplevel()
    win.title("Order Process Step")
    win.geometry("320x300")
    win.configure(bg="#f4f8fb")
    win.resizable(False, False)
    win.geometry(f"+{x}+{y}")

    frame = tk.Frame(win, bg="#f4f8fb")
    frame.pack(fill="both", expand=True, pady=15)

    steps = [
        "Product Research",
        "Shipment Schedule",
        "RCMC Process",
        "Communication Process (BOQ)"
    ]

    for step in steps:
        if step == "Communication Process (BOQ)":
            tk.Button(
                frame, text=step, width=32, height=2,
                bg="white", fg="#1f4e79",
                font=("Segoe UI", 10, "bold"),
                relief="solid", bd=1,
                command=lambda: open_boq_form(win)
            ).pack(pady=6)
        else:
            tk.Button(
                frame, text=step, width=32, height=2,
                bg="white", fg="#1f4e79",
                font=("Segoe UI", 10, "bold"),
                relief="solid", bd=1
            ).pack(pady=6)

def open_reports(x, y):
    win = tk.Toplevel()
    win.title("Reports")
    win.geometry("330x220")
    win.configure(bg="#f4f8fb")
    win.resizable(False, False)
    win.geometry(f"+{x}+{y}")

    frame = tk.Frame(win, bg="#f4f8fb")
    frame.pack(fill="both", expand=True, pady=20)

    tk.Button(
        frame,
        text="BOQ Buyer Master Analytics",
        width=34,
        height=2,
        bg="white",
        fg="#1f4e79",
        font=("Segoe UI", 10, "bold"),
        relief="solid",
        bd=1,
        command=lambda: open_boq_buyer_master(win)
    ).pack(pady=10)

    tk.Button(
        frame,
        text="Close",
        bg="#c0392b",
        fg="white",
        width=20,
        font=("Segoe UI", 10, "bold"),
        command=win.destroy
    ).pack(pady=15)


def open_progress(x, y):
    win = tk.Toplevel()
    win.title("Progress")
    win.geometry("330x350")
    win.configure(bg="#f4f8fb")
    win.resizable(False, False)
    win.geometry(f"+{x}+{y}")

    frame = tk.Frame(win, bg="#f4f8fb")
    frame.pack(fill="both", expand=True, pady=10)

    actions = {
        "MS Word": lambda: subprocess.Popen(["start", "winword"], shell=True),
        "MS Excel": lambda: subprocess.Popen(["start", "excel"], shell=True),
        "Calculator": lambda: subprocess.Popen(["calc"], shell=True)
    }

    for opt in ["File(s) Back-Up", "File(s) Re-Store", "Final Account Annual Posting",
                "MS Word", "MS Excel", "Calculator"]:
        tk.Button(
            frame, text=opt,
            width=34, height=2,
            bg="white", fg="#1f4e79",
            font=("Segoe UI", 10, "bold"),
            relief="solid", bd=1,
            command=actions.get(opt)
        ).pack(pady=4)

    tk.Button(frame, text="Exit", bg="#c0392b", fg="white",
              width=20, command=win.destroy).pack(pady=10)


def open_settings(x, y):
    win = tk.Toplevel()
    win.title("Settings")
    win.geometry("340x380")
    win.configure(bg="#f4f8fb")
    win.resizable(False, False)
    win.geometry(f"+{x}+{y}")

    frame = tk.Frame(win, bg="#f4f8fb")
    frame.pack(fill="both", expand=True, pady=10)

    for opt in [
        "File(s) Data Utilities",
        "Company Login",
        "Create Company",
        "Business Setup - 1",
        "Business Setup - 2",
        "Modify Authorization",
        "Modify Password",
        "Help Keys"
    ]:
        tk.Button(
            frame, text=opt,
            width=34, height=2,
            bg="white", fg="#1f4e79",
            font=("Segoe UI", 10, "bold"),
            relief="solid", bd=1
        ).pack(pady=4)

    tk.Button(frame, text="Exit", bg="#c0392b", fg="white",
              width=20, command=win.destroy).pack(pady=10)
