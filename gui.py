import tkinter as tk
from tkinter import Tk, ttk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
root = Tk()
root.title("My Banking App System")

def login(email, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Coisfun@2",
            database="banking"
        )
        if connection.is_connected():
            print("Connected to the database.")  # Debugging
            cursor = connection.cursor()
            # Query to fetch the user's name and email
            cursor.execute("SELECT name, email FROM customers WHERE email=%s AND password=%s", (email, password))
            result = cursor.fetchone()
            print(f"Query result: {result}")  # Debugging
            if result:
                name, email = result  # Extract name and email from the query result
                messagebox.showinfo("Login", "Login successful!")
                open_account_window(name, email)  # Open the account window
            else:
                messagebox.showerror("Login", "Invalid email or password.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

def sign_up(name, email, password, age):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Coisfun@2",
            database="banking"
        )
        if connection.is_connected():
            print("Connected to the database for sign-up.")  # Debugging
            cursor = connection.cursor()
            # Include the name column in the INSERT statement
            cursor.execute(
                "INSERT INTO customers (name, email, password, age) VALUES (%s, %s, %s, %s)",
                (name, email, password, age)
            )
            connection.commit()
            messagebox.showinfo("Sign-Up", "Sign-Up successful! You can now log in.")
    except Error as e:
        print(f"Error: {e}")
        messagebox.showerror("Sign-Up", "An error occurred during sign-up.")
    finally:
        if connection.is_connected():
            connection.close() 

def open_sign_up_window():
    # Create a new window for sign-up
    sign_up_window = tk.Toplevel(root)
    sign_up_window.title("Sign-Up")

    # Name field
    tk.Label(sign_up_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(sign_up_window)
    name_entry.pack(pady=5)

    # Email field
    tk.Label(sign_up_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(sign_up_window)
    email_entry.pack(pady=5)

    # Password field
    tk.Label(sign_up_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(sign_up_window, show="*")  # Mask password input
    password_entry.pack(pady=5)

    # Age field
    tk.Label(sign_up_window, text="Age:").pack(pady=5)
    age_entry = tk.Entry(sign_up_window)
    age_entry.pack(pady=5)

    def handle_sign_up():
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        age = age_entry.get()
        if name and email and password and age:
            sign_up(name, email, password, age)  # Save the user's details to the database
            sign_up_window.destroy()  # Close the sign-up window
            open_account_window(name, email)  # Open the account window
        else:
            messagebox.showerror("Sign-Up", "Please fill in all fields.")

    tk.Button(sign_up_window, text="Sign Up", command=handle_sign_up).pack(pady=10)

def button_click():
    # Get user input from the Entry widgets
    email = email_entry.get()
    password = password_entry.get()
    login(email, password)

# Create Entry widgets for email and password
tk.Label(root, text="Email:").pack(pady=5)
email_entry = tk.Entry(root)
email_entry.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")  # Mask password input
password_entry.pack(pady=5)

# Create the Login button
login_button = tk.Button(root, text="Login", command=button_click)
login_button.pack(pady=10)

# Create the Sign-Up button
sign_up_button = tk.Button(root, text="Sign Up", command=open_sign_up_window)
sign_up_button.pack(pady=10)

# Create a frame for additional widgets
frm = ttk.Frame(root)
frm.pack(pady=10)
ttk.Label(frm, text="Hi there, welcome to your bank!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

def open_account_window(name, email):
    # Create a new window for the user's account
    account_window = tk.Toplevel(root)
    account_window.title("My Account")

    # Display user details
    tk.Label(account_window, text=f"Welcome, {name}!", font=("Arial", 16)).pack(pady=10)
    tk.Label(account_window, text=f"Email: {email}", font=("Arial", 12)).pack(pady=5)

    # Add buttons for account actions
    tk.Button(account_window, text="Check Account", command=lambda: check_account(email)).pack(pady=10)
    tk.Button(account_window, text="Withdraw", command=lambda: withdraw(email)).pack(pady=10)
    tk.Button(account_window, text="Deposit", command=lambda: deposit(email)).pack(pady=10)
    tk.Button(account_window, text="Logout", command=account_window.destroy).pack(pady=10)

    def check_account(email):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Coisfun@2",
                database="banking"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                # Query to fetch the user's balance
                cursor.execute("SELECT balance FROM customers WHERE email=%s", (email,))
                result = cursor.fetchone()
                if result:
                    balance = result[0]  # Extract the balance from the query result
                    messagebox.showinfo("Account", f"Your balance is ${balance:.2f}")
                else:
                    messagebox.showerror("Account", "Account details not found.")
        except Error as e:
            messagebox.showerror("Account", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                connection.close()

def withdraw(email):
    def process_withdrawal():
        try:
            amount = float(amount_entry.get())
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Coisfun@2",
                database="banking"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                # Check current balance
                cursor.execute("SELECT balance FROM customers WHERE email=%s", (email,))
                result = cursor.fetchone()
                if result:
                    current_balance = result[0]
                    if amount > current_balance:
                        messagebox.showerror("Error", "Insufficient funds.")
                    else:
                        # Update balance
                        new_balance = current_balance - amount
                        cursor.execute("UPDATE customers SET balance=%s WHERE email=%s", (new_balance, email))
                        connection.commit()
                        messagebox.showinfo("Success", f"Withdrawal successful! New balance: ${new_balance:.2f}")
                        withdraw_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
        except Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                connection.close()

    # Create a new window for withdrawal
    withdraw_window = tk.Toplevel(root)
    withdraw_window.title("Withdraw Money")

    tk.Label(withdraw_window, text="Enter amount to withdraw:").pack(pady=5)
    amount_entry = tk.Entry(withdraw_window)
    amount_entry.pack(pady=5)
    tk.Button(withdraw_window, text="Withdraw", command=process_withdrawal).pack(pady=10)

def deposit(email):
    def process_deposit():
        try:
            amount = float(amount_entry.get())
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Coisfun@2",
                database="banking"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                # Check current balance
                cursor.execute("SELECT balance FROM customers WHERE email=%s", (email,))
                result = cursor.fetchone()
                if result:
                    current_balance = result[0]
                    # Update balance
                    new_balance = current_balance + amount
                    cursor.execute("UPDATE customers SET balance=%s WHERE email=%s", (new_balance, email))
                    connection.commit()
                    messagebox.showinfo("Success", f"Deposit successful! New balance: ${new_balance:.2f}")
                    deposit_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
        except Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                connection.close()

    # Create a new window for deposit
    deposit_window = tk.Toplevel(root)
    deposit_window.title("Deposit Money")

    tk.Label(deposit_window, text="Enter amount to deposit:").pack(pady=5)
    amount_entry = tk.Entry(deposit_window)
    amount_entry.pack(pady=5)
    tk.Button(deposit_window, text="Deposit", command=process_deposit).pack(pady=10)
root.mainloop()