import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
import reg  
import exp  
import admin  

class LoginPage:
    def __init__(self, root):
        self.root = root
        
        self.root.title("Expense Tracer | Login | Signup")
        
        # MongoDB connection
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['expense_tracker']
        self.auth_collection = self.db['auth']
    
        # Email Entry
        tk.Label(self.root, text="Enter Valid Email:").grid(row=0, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Password Entry
        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Login Button
        login_button = tk.Button(self.root, text="Login", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        
        # New User Button
        new_user_button = tk.Button(self.root, text="New User?", command=self.open_registration_page)
        new_user_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        
        # Dark Mode and Light Mode Checkbuttons
        self.mode_var = tk.StringVar(value="Light Mode")
        dark_mode_checkbutton = tk.Checkbutton(self.root, text="Dark Mode", variable=self.mode_var, onvalue="Dark Mode", offvalue="Light Mode")
        dark_mode_checkbutton.grid(row=4, column=0, padx=10, pady=5)
        light_mode_checkbutton = tk.Checkbutton(self.root, text="Light Mode", variable=self.mode_var, onvalue="Light Mode", offvalue="Dark Mode")
        light_mode_checkbutton.grid(row=4, column=1, padx=10, pady=5)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Check if the entered credentials are for the admin
        if email == "admin" and password == "adminpassword":
            self.root.destroy()
            root = tk.Tk()
            admin_page = admin.AdminPage(root)
            root.mainloop()
        else:
            # Query the database for the entered email and password
            user = self.auth_collection.find_one({'email_id': email, 'password': password})
            if user:
                # Close the login window
                self.root.destroy()
                
                # Open the expense tracker page
                root = tk.Tk()
                app = exp.ExpenseTrackerApp(root)
                root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid email or password.")
    
    def open_registration_page(self):
        # Open the registration page
        self.root.withdraw()  # Hide the login window
        root = tk.Tk()
        reg_page = reg.RegistrationPage(root, self)
        root.mainloop()
        self.root.deiconify()  # Show the login window again after registration

def main():
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
