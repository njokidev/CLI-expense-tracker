from dataclasses import dataclass
from db import get_connection


@dataclass
class Expense:
    id: int
    amount: float
    category: str
    note: str
    date: str

    @classmethod
    def create(cls, amount, category, note, date):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        if not category:
            raise ValueError("Category cannot be empty")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO expenses (amount, category, note, date)
            VALUES (?, ?, ?, ?)
            """,
            (amount, category, note, date)
        )

        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()

        return cls(expense_id, amount, category, note, date)

    @classmethod
    def list_all(cls):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()

        return [
            cls(row["id"], row["amount"], row["category"], row["note"], row["date"])
            for row in rows
        ]

    @classmethod
    def delete(cls, expense_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

        conn.commit()
        conn.close()

    @classmethod
    def list_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM expenses WHERE category = ?",
            (category,)
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            cls(row["id"], row["amount"], row["category"], row["note"], row["date"])
            for row in rows
        ]

    @classmethod
    def update(cls, expense_id, amount, category, note, date):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE expenses
            SET amount=?, category=?, note=?, date=?
            WHERE id=?
        """, (amount, category, note, date, expense_id))

        conn.commit()
        conn.close()