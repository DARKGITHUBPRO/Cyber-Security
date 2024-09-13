import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# إنشاء قاعدة البيانات
conn = sqlite3.connect('company.db')
c = conn.cursor()

# إنشاء جدول الموظفين
c.execute('''CREATE TABLE IF NOT EXISTS employees (
             id INTEGER PRIMARY KEY,
             name TEXT,
             position TEXT,
             salary REAL)''')

# إنشاء جدول العملاء
c.execute('''CREATE TABLE IF NOT EXISTS clients (
             id INTEGER PRIMARY KEY,
             name TEXT,
             email TEXT,
             phone TEXT)''')

# إنشاء جدول الفواتير
c.execute('''CREATE TABLE IF NOT EXISTS invoices (
             id INTEGER PRIMARY KEY,
             client_id INTEGER,
             amount REAL,
             date TEXT,
             FOREIGN KEY(client_id) REFERENCES clients(id))''')

# إنشاء جدول المديرين
c.execute('''CREATE TABLE IF NOT EXISTS managers (
             id INTEGER PRIMARY KEY,
             username TEXT,
             password TEXT)''')

# إضافة مدير افتراضي
c.execute("INSERT INTO managers (username, password) VALUES (?, ?)", ('admin', 'admin123'))
conn.commit()

# دالة لتسجيل الدخول
def login():
    username = entry_username.get()
    password = entry_password.get()
    c.execute("SELECT * FROM managers WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    if result:
        messagebox.showinfo("Success", "Login successful")
        open_dashboard()
    else:
        messagebox.showerror("Error", "Invalid username or password")

# دالة لفتح لوحة التحكم
def open_dashboard():
    dashboard = tk.Toplevel(root)
    dashboard.title("Manager Dashboard")
    dashboard.configure(bg='#34495e')

    tabControl = ttk.Notebook(dashboard)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)

    tabControl.add(tab1, text='Employees')
    tabControl.add(tab2, text='Clients')
    tabControl.add(tab3, text='Invoices')

    tabControl.pack(expand=1, fill="both")

    # تبويب الموظفين
    tk.Label(tab1, text="Employee Name", font=('Helvetica', 12, 'bold'), bg='#ecf0f1').grid(row=0, pady=5)
    tk.Label(tab1, text="Position", font=('Helvetica', 12, 'bold'), bg='#ecf0f1').grid(row=1, pady=5)
    tk.Label(tab1, text="Salary", font=('Helvetica', 12, 'bold'), bg='#ecf0f1').grid(row=2, pady=5)

    global entry_name, entry_position, entry_salary
    entry_name = ttk.Entry(tab1, width=30)
    entry_position = ttk.Entry(tab1, width=30)
    entry_salary = ttk.Entry(tab1, width=30)

    entry_name.grid(row=0, column=1, padx=10, pady=5)
    entry_position.grid(row=1, column=1, padx=10, pady=5)
    entry_salary.grid(row=2, column=1, padx=10, pady=5)

    ttk.Button(tab1, text='Add Employee', command=add_employee).grid(row=3, column=1, sticky=tk.W, pady=10)
    ttk.Button(tab1, text='Print Employees', command=print_employees).grid(row=4, column=1, sticky=tk.W, pady=10)
    ttk.Button(tab1, text='Save Employee', command=save_employee).grid(row=5, column=1, sticky=tk.W, pady=10)

    # تبويب العملاء
    tk.Label(tab2, text="Client Name", font=('Helvetica', 12, 'bold'), bg='#ecf0f1').grid(row=0, pady=5)
    tk.Label(tab2, text="Email", font=('Helvetica', 12, 'bold'), bg='#ecf0f1').grid(row=1, pady=5)
    tk.Label(tab2, text="Phone", font=('Helvetica', 12, 'bold'), bg='#ecf0f1').grid(row=2, pady=5)

    global entry_client_name, entry_client_email, entry_client_phone
    entry_client_name = ttk.Entry(tab2, width=30)
    entry_client_email = ttk.Entry(tab2, width=30)
    entry_client_phone = ttk.Entry(tab2, width=30)

    entry_client_name.grid(row=0, column=1, padx=10, pady=5)
    entry_client_email.grid(row=1, column=1, padx=10, pady=5)
    entry_client_phone.grid(row=2, column=1, padx=10, pady=5)

    ttk.Button(tab2, text='Add Client', command=add_client).grid(row=3, column=1, sticky=tk.W, pady=10)

    # تبويب الفواتير
    tk.Label(tab3, text="Client ID", font=('Helvetica', 12, 'bold'), bg='#ecf0f1').grid(row=0, pady=5)
    tk.Label(tab3, text="Amount", font=('Helvetica', 12, 'bold'), bg='#ecf0f1').grid(row=1, pady=5)
    tk.Label(tab3, text="Date", font=('Helvetica', 12, 'bold'), bg='#ecf0f1').grid(row=2, pady=5)

    global entry_invoice_client_id, entry_invoice_amount, entry_invoice_date
    entry_invoice_client_id = ttk.Entry(tab3, width=30)
    entry_invoice_amount = ttk.Entry(tab3, width=30)
    entry_invoice_date = ttk.Entry(tab3, width=30)

    entry_invoice_client_id.grid(row=0, column=1, padx=10, pady=5)
    entry_invoice_amount.grid(row=1, column=1, padx=10, pady=5)
    entry_invoice_date.grid(row=2, column=1, padx=10, pady=5)

    def add_invoice():
        client_id = entry_invoice_client_id.get()
        amount = entry_invoice_amount.get()
        date = entry_invoice_date.get()
        c.execute("INSERT INTO invoices (client_id, amount, date) VALUES (?, ?, ?)", (client_id, amount, date))
        conn.commit()
        messagebox.showinfo("Success", "Invoice added successfully")

    ttk.Button(tab3, text='Add Invoice', command=add_invoice).grid(row=3, column=1, sticky=tk.W, pady=10)
    ttk.Button(tab3, text='Print Invoices', command=print_invoices).grid(row=4, column=1, sticky=tk.W, pady=10)

# دالة لإضافة موظف جديد
def add_employee():
    name = entry_name.get()
    position = entry_position.get()
    salary = entry_salary.get()
    c.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)", (name, position, salary))
    conn.commit()
    messagebox.showinfo("Success", "Employee added successfully")

# دالة لحفظ بيانات الموظف
def save_employee():
    name = entry_name.get()
    position = entry_position.get()
    salary = entry_salary.get()
    c.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)", (name, position, salary))
    conn.commit()
    messagebox.showinfo("Success", "Employee data saved successfully")

# دالة لحفظ بيانات الموظفين في ملف نصي
def save_employees():
    with open('employees.txt', 'w') as f:
        c.execute("SELECT * FROM employees")
        employees = c.fetchall()
        for emp in employees:
            f.write(f"ID: {emp[0]}, Name: {emp[1]}, Position: {emp[2]}, Salary: {emp[3]}\n")
    messagebox.showinfo("Success", "Employees data saved successfully")

# دالة لطباعة معلومات الموظفين
def print_employees():
    c.execute("SELECT * FROM employees")
    employees = c.fetchall()
    for emp in employees:
        print(emp)

# دالة لطباعة معلومات الفواتير
def print_invoices():
    c.execute("SELECT * FROM invoices")
    invoices = c.fetchall()
    invoice_window = tk.Toplevel(root)
    invoice_window.title("Invoices")
    invoice_window.configure(bg='#ecf0f1')

    for invoice in invoices:
        tk.Label(invoice_window, text=f"ID: {invoice[0]}, Client ID: {invoice[1]}, Amount: {invoice[2]}, Date: {invoice[3]}", bg='#ecf0f1').pack()

# دالة لإضافة عميل جديد
def add_client():
    name = entry_client_name.get()
    email = entry_client_email.get()
    phone = entry_client_phone.get()
    c.execute("INSERT INTO clients (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
    conn.commit()
    messagebox.showinfo("Success", "Client added successfully")

# إنشاء واجهة تسجيل الدخول
root = tk.Tk()
root.title("Company Management System - Login")
root.configure(bg='#2c3e50')

entry_username = ttk.Entry(root, width=30)
entry_password = ttk.Entry(root, show='*', width=30)

entry_username.grid(row=0, column=1, padx=10, pady=5)
entry_password.grid(row=1, column=1, padx=10, pady=5)

ttk.Button(root, text='Login', command=login).grid(row=2, column=1, sticky=tk.W, pady=10,padx=70)

root.mainloop()