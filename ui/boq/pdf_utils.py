import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def save_letter_as_pdf(letter_text, file_name, sub_folder):
    """
    Saves letter text as PDF inside reports/<sub_folder>/
    Returns full file path
    """

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    reports_dir = os.path.join(BASE_DIR, "reports", sub_folder)
    os.makedirs(reports_dir, exist_ok=True)

    file_path = os.path.join(reports_dir, file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    x = 1 * inch
    y = height - 1 * inch

    for line in letter_text.split("\n"):
        c.drawString(x, y, line)
        y -= 14

        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch

    c.save()
    return file_path
