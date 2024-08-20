import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

class RegistrationPage:
    def __init__(self, root, login_page):
        self.root = root
        self.login_page = login_page
        
        self.root.title("Expense Tracer | Registration")
        
        # MongoDB connection
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['expense_tracker']
        self.register_collection = self.db['register']
        self.auth_collection = self.db['auth']
        
        # Email Entry
        tk.Label(self.root, text="Enter Email:").grid(row=0, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # First Name Entry
        tk.Label(self.root, text="First Name:").grid(row=1, column=0, padx=10, pady=5)
        self.first_name_entry = tk.Entry(self.root)
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Last Name Entry
        tk.Label(self.root, text="Last Name:").grid(row=2, column=0, padx=10, pady=5)
        self.last_name_entry = tk.Entry(self.root)
        self.last_name_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Age Entry
        tk.Label(self.root, text="Age:").grid(row=3, column=0, padx=10, pady=5)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Password Entry
        tk.Label(self.root, text="Password:").grid(row=4, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Confirm Password Entry
        tk.Label(self.root, text="Confirm Password:").grid(row=5, column=0, padx=10, pady=5)
        self.confirm_password_entry = tk.Entry(self.root, show="*")
        self.confirm_password_entry.grid(row=5, column=1, padx=10, pady=5)
        
        # Register Button
        register_button = tk.Button(self.root, text="Register", command=self.register)
        register_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def register(self):
        email = self.email_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        age = self.age_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Check if email already exists
        if self.auth_collection.find_one({'email_id': email}):
            messagebox.showerror("Error", "Email already exists.")
            return

        # Insert user data into registration collection
        self.register_collection.insert_one({
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "password": password
        })

        # Insert email and password into auth collection
        self.auth_collection.insert_one({
            "email_id": email,
            "password": password
        })

        messagebox.showinfo("Success", "Registration successful.")
        self.root.destroy()  # Close the registration window

        # Open the login window after successful registration
        self.login_page.root.deiconify()

def main():
    root = tk.Tk()
    registration_page = RegistrationPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
