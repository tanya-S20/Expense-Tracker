import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

FILE_NAME = "expenses.txt"
expenses = []

# Categories to choose from
categories = ["Food", "Travel", "Shopping", "Bills", "Others"]

def add_expense():
    name = entry_name.get()
    amount = entry_amount.get()
    date = datetime.now().strftime("%Y-%m-%d")
    category = category_var.get()

    if name == "" or amount == "":
        messagebox.showwarning("Input Error", "Please enter both name and amount.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number.")
        return

    expenses.append((name, amount, date, category))
    save_expenses_to_file()
    update_expense_list()

    entry_name.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    category_var.set(categories[0])

def delete_expense():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select an expense to delete.")
        return

    index = selected[0]
    del expenses[index]
    save_expenses_to_file()
    update_expense_list()

def clear_all_expenses():
    confirm = messagebox.askyesno("Clear All", "Are you sure you want to delete all expenses?")
    if confirm:
        expenses.clear()
        save_expenses_to_file()
        update_expense_list()

def save_expenses_to_file():
    with open(FILE_NAME, "w") as f:
        for name, amount, date, category in expenses:
            f.write(f"{name},{amount},{date},{category}\n")

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return
    with open(FILE_NAME, "r") as f:
        for line in f:
            try:
                name, amount, date, category = line.strip().split(",")
                expenses.append((name, float(amount), date, category))
            except:
                continue

def update_expense_list():
    listbox.delete(0, tk.END)
    total = 0
    for name, amount, date, category in expenses:
        listbox.insert(tk.END, f"{name} - ₹{amount} - {category} ({date})")
        total += amount
    label_total.config(text=f"Total: ₹{total}")

# GUI setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x560")
root.resizable(False, False)

# Name input
label_name = tk.Label(root, text="Expense Name:")
label_name.pack(pady=(10, 2))
entry_name = tk.Entry(root, width=30)
entry_name.pack()

# Amount input
label_amount = tk.Label(root, text="Amount (₹):")
label_amount.pack(pady=(10, 2))
entry_amount = tk.Entry(root, width=30)
entry_amount.pack()

# Category dropdown
label_category = tk.Label(root, text="Select Category:")
label_category.pack(pady=(10, 2))
category_var = tk.StringVar()
category_var.set(categories[0])
dropdown = tk.OptionMenu(root, category_var, *categories)
dropdown.pack()

# Add expense
btn_add = tk.Button(root, text="Add Expense", command=add_expense)
btn_add.pack(pady=10)

# List of expenses
listbox = tk.Listbox(root, width=45, height=10)
listbox.pack(pady=10)

# Delete and clear buttons
btn_delete = tk.Button(root, text="Delete Selected", command=delete_expense)
btn_delete.pack(pady=5)

btn_clear_all = tk.Button(root, text="Clear All Expenses", command=clear_all_expenses, bg="red", fg="white")
btn_clear_all.pack(pady=5)

# Total label
label_total = tk.Label(root, text="Total: ₹0", font=("Arial", 12, "bold"))
label_total.pack(pady=(10, 5))

# Load and run
load_expenses()
update_expense_list()

root.mainloop()

