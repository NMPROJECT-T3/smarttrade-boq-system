import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "boq_system.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Add missing columns safely
try:
    cur.execute("ALTER TABLE boq_master ADD COLUMN boq_confirmed INTEGER DEFAULT 0")
except:
    pass

try:
    cur.execute("ALTER TABLE boq_master ADD COLUMN boq_confirmed_date TEXT")
except:
    pass

try:
    cur.execute("ALTER TABLE boq_master ADD COLUMN stage TEXT")
except:
    pass

conn.commit()
conn.close()

print("BOQ columns added successfully.")
