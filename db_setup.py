import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "boq_system.db")

os.makedirs(DB_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ===================== MASTER TABLE =====================
cur.execute("""
CREATE TABLE IF NOT EXISTS boq_master (
    booking_ref TEXT PRIMARY KEY,

    buyer_name TEXT,
    email TEXT,
    phone TEXT,
    country TEXT,
    region TEXT,

    product_name TEXT,
    priority TEXT,

    created_date TEXT,

    stage TEXT,  -- INITIAL / REMINDER / MOQ / BOQ
    reminder_count INTEGER DEFAULT 0,

    buyer_responded INTEGER DEFAULT 0,
    moq_sent INTEGER DEFAULT 0,
    boq_confirmed INTEGER DEFAULT 0
);
""")

conn.commit()
conn.close()

print("Fresh BOQ database created successfully.")
