import argparse
from datetime import date
from tabulate import tabulate
from expense import Expense

def print_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    table = [
        [e.id, e.amount, e.category, e.note, e.date]
        for e in expenses
    ]

    print(tabulate(table, headers=["ID", "Amount", "Category", "Note", "Date"]))

def handle_add(args):
    expense = Expense.create(
        amount=args.amount,
        category=args.category,
        note=args.note or "",
        date=args.date or str(date.today())
    )

    print(f"✅ Added expense with ID {expense.id}")

def handle_list(args):
    if args.category:
        expenses = Expense.list_by_category(args.category)
    else:
        expenses = Expense.list_all()

    print_expenses(expenses)

def handle_delete(args):
    Expense.delete(args.id)
    print(f"🗑️ Deleted expense with ID {args.id}")

def handle_report(args):
    from db import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE substr(date, 1, 7) = ?
        GROUP BY category
    """, (args.month,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No data for this month.")
        return

    table = [[row["category"], row["total"]] for row in rows]
    print(tabulate(table, headers=["Category", "Total"]))

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")

    subparsers = parser.add_subparsers(dest="command")

    # ➕ ADD
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--category", type=str, required=True)
    add_parser.add_argument("--note", type=str)
    add_parser.add_argument("--date", type=str)
    add_parser.set_defaults(func=handle_add)

    # 📋 LIST
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--category", type=str)
    list_parser.set_defaults(func=handle_list)

    # ❌ DELETE
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)
    delete_parser.set_defaults(func=handle_delete)

    # 📊 REPORT
    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("--month", type=str, required=True)
    report_parser.set_defaults(func=handle_report)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()