import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import pymysql

__db_endpoint = "minorproject2.cxcy0guqwtrx.eu-north-1.rds.amazonaws.com"
__db_user = "admin"
__db_pass = "13A&23k#"
__db_name = "db1"
__db_port = 3306

conn_db = pymysql.connect(
    host=__db_endpoint,
    user=__db_user,
    password=__db_pass,
    database=__db_name,
    port=__db_port,
)


import proto_v0_1

conn = sqlite3.connect("finanace.db")
cursor = conn.cursor()
backend = proto_v0_1.operations(conn, cursor)


# Function to display income or expense data
def display_data_expense():
    records = cursor.execute(
        "select b.date,amount,party_2 from bank_transactions as b inner join not_spam_sms as s on s.rowid=b.id inner join regex as r on r.id=s.regexID where r.debit=1 order by b.id desc;"
    ).fetchall()

    window = tk.Toplevel()
    window.title(f"Expense Records")

    tree = ttk.Treeview(window, columns=("Date", "Amount", "Send To"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Amount", text="Amount")
    tree.heading("Send To", text="Send To")

    tree.pack(fill=tk.BOTH, expand=True)

    for row in records:
        tree.insert("", tk.END, values=row)


# Function to display income or expense data
def display_data_income():
    records = cursor.execute(
        "select b.date,amount,party_2 from bank_transactions as b inner join not_spam_sms as s on s.rowid=b.id inner join regex as r on r.id=s.regexID where r.debit=0 order by b.id desc ;"
    ).fetchall()

    window = tk.Toplevel()
    window.title(f"Income Records")

    tree = ttk.Treeview(window, columns=("Date", "Amount", "Sender"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Amount", text="Amount")
    tree.heading("Sender", text="Sender")

    tree.pack(fill=tk.BOTH, expand=True)

    for row in records:
        tree.insert("", tk.END, values=row)


# Function to update income and expense amounts
def update_numbers():

    command = "select sum(amount) as amt from bank_transactions as b inner join not_spam_sms as s on s.rowid=b.id inner join regex as r on r.id=s.regexID group by r.debit having r.debit=0;"
    resp = cursor.execute(command).fetchall()

    income, expense = 0, 0
    if len(resp) > 0:
        income = resp[0][0]

    command = "select sum(amount) as amt from bank_transactions as b inner join not_spam_sms as s on s.rowid=b.id inner join regex as r on r.id=s.regexID group by r.debit having r.debit=1;"
    resp = cursor.execute(command).fetchall()

    if len(resp) > 0:
        expense = resp[0][0]

    # income = sum([r[1] for r in fetch_data("income")])
    # expense = sum([r[1] for r in fetch_data("expense")])

    income_button.config(text=f"Income: ${income:.2f}")
    expense_button.config(text=f"Expense: ${expense:.2f}")


# Function to handle submit button
def submit_data():

    message = amount_entry.get(1.0, "end-1c")
    backend.main(message)

    update_numbers()


def refresh():
    with conn_db.cursor() as cursor:
        query = "select * from queue where read_status=false;"
        cursor.execute(query)
        result = cursor.fetchall()

        unread_sl_list = []

        for row in result:
            unread_sl_list.append(row[0])
            print(row[1], " ", row[3])
            backend.main(row[1], sender=row[3])

        for sl in unread_sl_list:
            query = f"update queue set read_status=true where sl={sl};"
            cursor.execute(query)
            conn_db.commit()

        update_numbers()


# Main window setup
root = tk.Tk()
root.title("Income and Expense Tracker")
"""

# Textbox for amount entry (larger size)
amount_entry = tk.Text(root, height=10, width=60)
amount_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Income button
income_button = tk.Button(
    root,
    text="Income: $0.00",
    bg="green",
    fg="white",
    command=lambda: display_data_income(),
)
income_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Expense button
expense_button = tk.Button(
    root,
    text="Expense: $0.00",
    bg="red",
    fg="white",
    command=lambda: display_data_expense(),
)
expense_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Submit button (side by side with income and expense buttons)
submit_button = tk.Button(root, text="Submit", command=submit_data)
submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
"""
amount_entry = tk.Text(root, height=10, width=60)
amount_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Income button
income_button = tk.Button(
    root,
    text="Income: $0.00",
    bg="green",
    fg="white",
    command=lambda: display_data_income(),
)
income_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Expense button
expense_button = tk.Button(
    root,
    text="Expense: $0.00",
    bg="red",
    fg="white",
    command=lambda: display_data_expense(),
)
expense_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Submit button (side by side with income and expense buttons)
submit_button = tk.Button(root, text="Submit", command=submit_data)
submit_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# Refresh button beside submit button
refresh_button = tk.Button(root, text="Refresh", command=refresh)
refresh_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# Initialize the database and update income and expense
update_numbers()

root.mainloop()
