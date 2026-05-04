import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "expenses.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        amount  REAL  NOT NULL,
        category  TEXT NOT NULL,
        note TEXT,
        date TEXT NOT NULL);
        """)
    
    conn.commit()
    conn.close()

init_db()