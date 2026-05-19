import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "boq_system.db")

os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS boq_reference (
    booking_ref TEXT PRIMARY KEY,
    buyer_name TEXT,
    contact TEXT,
    reference_from TEXT,
    country TEXT,
    region TEXT,
    created_date TEXT,

    reminder_count INTEGER DEFAULT 0,
    buyer_responded INTEGER DEFAULT 0,

    moq_sent INTEGER DEFAULT 0,
    moq_date TEXT,
    moq_product TEXT
);
""")

conn.commit()
conn.close()

print("boq_reference table created successfully.")
