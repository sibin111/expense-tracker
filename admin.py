import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from bson import ObjectId

class AdminPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Page")

        # MongoDB setup
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['expense_tracker']
        self.register_collection = self.db['register']

        # Table to display user details
        self.users_table = ttk.Treeview(self.root, columns=("ID", "First Name", "Last Name", "Email", "Age", "Password"), show="headings")
        self.users_table.heading("ID", text="ID")
        self.users_table.heading("First Name", text="First Name")
        self.users_table.heading("Last Name", text="Last Name")
        self.users_table.heading("Email", text="Email")
        self.users_table.heading("Age", text="Age")
        self.users_table.heading("Password", text="Password")
        self.users_table.pack(fill="both", expand=True)

        # Populate the table with user details
        self.populate_table()

        # Buttons for editing and removing users
        edit_button = tk.Button(self.root, text="Edit", command=self.edit_user)
        edit_button.pack(side="left", padx=5, pady=5)
        
        remove_button = tk.Button(self.root, text="Remove", command=self.remove_user)
        remove_button.pack(side="left", padx=5, pady=5)
        
        # Logout Button
        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(side="right", padx=5, pady=5)

    def populate_table(self):
        # Clear existing rows
        for row in self.users_table.get_children():
            self.users_table.delete(row)
        
        # Retrieve user details from MongoDB
        users = self.register_collection.find({})
        for user in users:
            self.users_table.insert("", "end", values=(str(user["_id"]), user["first_name"], user["last_name"], user["email"], user["age"], user["password"]))

    def edit_user(self):
        # Get the selected user's ID
        selected_item = self.users_table.selection()
        if selected_item:
            user_id = self.users_table.item(selected_item, "values")[0]
            # Open a window for editing user details
            edit_window = tk.Toplevel(self.root)
            tk.Label(edit_window, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
            tk.Label(edit_window, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
            tk.Label(edit_window, text="Email:").grid(row=2, column=0, padx=5, pady=5)
            tk.Label(edit_window, text="Age:").grid(row=3, column=0, padx=5, pady=5)
            tk.Label(edit_window, text="Password:").grid(row=4, column=0, padx=5, pady=5)
            # Get current values
            current_values = self.users_table.item(selected_item, "values")[1:]  # Exclude ID
            entry_widgets = {}
            for i, value in enumerate(current_values):
                entry_widgets[i] = tk.Entry(edit_window)
                entry_widgets[i].insert(0, value)
                entry_widgets[i].grid(row=i, column=1, padx=5, pady=5)
            # Button to save changes
            save_button = tk.Button(edit_window, text="Save", command=lambda: self.save_changes(user_id, entry_widgets, edit_window))
            save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        else:
            messagebox.showerror("Error", "Please select a user to edit.")

    def save_changes(self, user_id, entry_widgets, edit_window):
        # Get the edited values from the entry widgets
        edited_values = {}
        keys = ["first_name", "last_name", "email", "age", "password"]
        for i, entry_widget in entry_widgets.items():
            edited_values[keys[i]] = entry_widget.get()
        
        try:
            # Update the user details in the database
            self.register_collection.update_one({"_id": ObjectId(user_id)}, {"$set": edited_values})
            messagebox.showinfo("Success", "User details updated successfully.")
            # Refresh the table
            self.populate_table()
            # Close the edit window
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def remove_user(self):
        # Get the selected user's ID
        selected_item = self.users_table.selection()
        if selected_item:
            user_id = self.users_table.item(selected_item, "values")[0]
            # Ask for confirmation before removing the user
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove this user?")
            if confirmation:
                try:
                    # Remove the user from the database
                    self.register_collection.delete_one({"_id": ObjectId(user_id)})
                    messagebox.showinfo("Success", "User removed successfully.")
                    # Refresh the table
                    self.populate_table()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Please select a user to remove.")

    def logout(self):
        self.root.destroy()
        import loginpage # Make sure login.py is available
        root = tk.Tk()
        login_page = loginpage.LoginPage(root)
        root.mainloop()

def main():
    root = tk.Tk()
    admin_page = AdminPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
