import tkinter as tk
from tkinter import simpledialog, messagebox

class Account:
    def __init__(self, pin, balance=0):
        self.pin = pin
        self.balance = balance
        self.transactions = []

    def record_transaction(self, description):
        self.transactions.append(description)

class TransactionHistory:
    @staticmethod
    def show_history(account):
        trans = "\n".join(account.transactions)
        messagebox.showinfo("Transaction History", f"Transactions:\n{trans}")

class Withdraw:
    @staticmethod
    def withdraw_money(account, amount):
        if account.balance >= amount:
            account.balance -= amount
            account.record_transaction(f"Withdrew ${amount}")
            messagebox.showinfo("Success", f"${amount} has been withdrawn.")
        else:
            messagebox.showerror("Error", "Insufficient funds")

# Class to handle deposit functionality
class Deposit:
    @staticmethod
    def deposit_money(account, amount):
        account.balance += amount
        account.record_transaction(f"Deposited ${amount}")
        messagebox.showinfo("Success", f"${amount} has been deposited.")

class Transfer:
    @staticmethod
    def transfer_money(src_account, dest_account, amount):
        if src_account.balance >= amount:
            src_account.balance -= amount
            dest_account.balance += amount
            src_account.record_transaction(f"Transferred ${amount} to another account")
            dest_account.record_transaction(f"Received ${amount} from another account")
            messagebox.showinfo("Success", f"Transferred ${amount} to another account")
        else:
            messagebox.showerror("Error", "Insufficient funds")

class ATMInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM Interface")
        self.master.geometry("500x500")

        # Configure rows and columns for layout
        for i in range(6):
            self.master.grid_rowconfigure(i, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.accounts = {
            "1234": Account("1234", 5000),
            "4567": Account("4567", 10000),
            "7890": Account("7890", 15000),
        }

        self.create_login_window()

    def create_login_window(self):
        # Clear any existing widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Welcome message
        welcome_label = tk.Label(self.master, text="Welcome!  Please insert your card.", font=("Helvetica", 14))
        welcome_label.grid(row=0, columnspan=2, pady=20)

        # Title
        title = tk.Label(self.master, text="Please insert your pin", font=("Helvetica", 16))
        title.grid(row=1, columnspan=2, pady=10)

        tk.Label(self.master, text="PIN").grid(row=2, column=0, padx=20, pady=10)

        self.e1 = tk.Entry(self.master, show="*")

        self.e1.grid(row=2, column=1, padx=20, pady=10)

        tk.Button(self.master, text="Quit", command=self.master.destroy).grid(row=4, columnspan=2, pady=5)

        tk.Button(self.master, text="Login", command=self.login).grid(row=3, columnspan=2, pady=5)

    def login(self):
        pin = self.e1.get()

        if pin in self.accounts and self.accounts[pin].pin == pin:
            self.current_account = self.accounts[pin]
            messagebox.showinfo("Success", "Continue login")
            self.show_options()
        else:
            messagebox.showerror("Error", "Invalid PIN")

    def show_options(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        title = tk.Label(self.master, text="Please Choose the Services", font=("Helvetica", 16))
        title.grid(row=0, columnspan=2, pady=20)

        tk.Button(self.master, text="Current Balance", command=self.show_balance).grid(row=1, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Transactions History", command=lambda: TransactionHistory.show_history(self.current_account)).grid(row=2, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Withdraw", command=self.withdraw_money_gui).grid(row=3, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Deposit", command=self.deposit_money_gui).grid(row=4, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Transfer", command=self.transfer_money_gui).grid(row=5, columnspan=2, padx=20, pady=5)
        tk.Button(self.master, text="Quit", command=self.master.destroy).grid(row=6, columnspan=2, padx=20, pady=5)

    def show_balance(self):
        messagebox.showinfo("Current Balance", f"Your current balance is ${self.current_account.balance}")

    def withdraw_money_gui(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is not None:
            Withdraw.withdraw_money(self.current_account, amount)

    def deposit_money_gui(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is not None:
            Deposit.deposit_money(self.current_account, amount)

    def transfer_money_gui(self):
        transfer_pin = simpledialog.askstring("Transfer", "Enter PIN of the account to transfer to:")
        if transfer_pin in self.accounts:
            amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")
            if amount is not None:
                Transfer.transfer_money(self.current_account, self.accounts[transfer_pin], amount)
        else:
            messagebox.showerror("Error", "Invalid PIN")

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMInterface(root)
    root.mainloop()
