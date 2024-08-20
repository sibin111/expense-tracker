import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from datetime import datetime
from tkcalendar import Calendar
from bson import ObjectId 
from report import ReportPage

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        
        # MongoDB setup
        try:
            self.client = MongoClient('mongodb://localhost:27017/')
            self.db = self.client['expense_tracker']
            self.collection = self.db['expenses']  # Changed collection name to 'expenses'
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to MongoDB: {e}")
            return
        
        # Initialize the expense tracker page
        self.init_expense_tracker_page()
    
    def init_expense_tracker_page(self):
        # Expense Tracker Input Page Elements
        tk.Label(self.root, text="Type:").grid(row=0, column=0, padx=10, pady=5)
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(self.root, textvariable=self.type_var, 
                                          values=["Income", "Savings", "Expense"])
        self.type_dropdown.grid(row=0, column=1, padx=10, pady=5)
        self.type_dropdown.current(0)
        
        tk.Label(self.root, text="Category:").grid(row=1, column=0, padx=10, pady=5)
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.root, textvariable=self.category_var, 
                                               values=["Salary", "Source 2", "Mutual Funds", "Emergency Fund",
                                                       "Fixed Deposit", "Liquid Cash", "House Rent", 
                                                       "Groceries and Food", "Health", "EMIs", 
                                                       "Leisure", "Shopping"])
        self.category_dropdown.grid(row=1, column=1, padx=10, pady=5)
        self.category_dropdown.current(0)
        
        tk.Label(self.root, text="Date:").grid(row=2, column=0, padx=10, pady=5)
        self.date_picker = Calendar(self.root, selectmode="day", year=datetime.now().year,
                                    month=datetime.now().month, day=datetime.now().day)
        self.date_picker.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Amount:").grid(row=3, column=0, padx=10, pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Buttons for CRUD operations
        save_button = tk.Button(self.root, text="Save", command=self.save_transaction)
        save_button.grid(row=4, column=0, padx=10, pady=5)
        
        delete_button = tk.Button(self.root, text="Delete", command=self.delete_transaction)
        delete_button.grid(row=4, column=1, padx=10, pady=5)
        
        update_button = tk.Button(self.root, text="Update", command=self.update_transaction)
        update_button.grid(row=4, column=2, padx=10, pady=5)
        
        # Table to display transactions
        self.transactions_tree = ttk.Treeview(self.root, columns=("Type", "Category", "Date", "Amount", "ID"), show="headings")
        self.transactions_tree.heading("Type", text="Type")
        self.transactions_tree.heading("Category", text="Category")
        self.transactions_tree.heading("Date", text="Date")
        self.transactions_tree.heading("Amount", text="Amount")
        self.transactions_tree.heading("ID", text="ID")
        self.transactions_tree.grid(row=5, column=0, columnspan=4, padx=10, pady=5)
        
        # Bind double-click event to select row for update
        self.transactions_tree.bind("<Double-1>", self.on_double_click)
        
        # Populate the table with existing transactions
        self.populate_table()
        
        # Button to navigate to the report page
        report_button = tk.Button(self.root, text="View Report", command=self.open_report_page)
        report_button.grid(row=6, column=0, columnspan=4, padx=10, pady=5)
    
    def populate_table(self):
        # Clear existing rows
        for row in self.transactions_tree.get_children():
            self.transactions_tree.delete(row)
        
        # Retrieve transactions from MongoDB
        transactions = self.collection.find({})
        for transaction in transactions:
            if "Type" in transaction and "Category" in transaction and "Date" in transaction and "Amount" in transaction:
                self.transactions_tree.insert("", "end", values=(transaction["Type"], 
                                                                transaction["Category"], 
                                                                transaction["Date"], 
                                                                transaction["Amount"], 
                                                                str(transaction["_id"])))
    
    def save_transaction(self):
        try:
            # Get data from input fields
            type_value = self.type_var.get()
            category_value = self.category_var.get()
            amount_value_str = self.amount_entry.get()
            date_value = self.date_picker.get_date()
            
            # Validate amount
            if not amount_value_str:
                raise ValueError("Amount cannot be empty.")
            amount_value = float(amount_value_str)
            
            # Format date
            formatted_date = datetime.strptime(date_value, "%m/%d/%y").strftime("%d/%m/%y")
            
            # Save data to MongoDB
            self.collection.insert_one({
                "Type": type_value,
                "Category": category_value,
                "Date": formatted_date,
                "Amount": amount_value
            })
            # Show a message indicating successful save
            messagebox.showinfo("Success", "Transaction saved successfully.")
            # Refresh the table
            self.populate_table()
        except Exception as e:
            messagebox.showerror("Error", f"Error saving transaction: {e}")
    
    def delete_transaction(self):
        try:
            # Get selected item from the table
            selected_item = self.transactions_tree.selection()
            if selected_item:
                # Get transaction ID from the selected item
                transaction_id = self.transactions_tree.item(selected_item, "values")[4]
                
                # Delete the transaction from MongoDB
                self.collection.delete_one({"_id": ObjectId(transaction_id)})
                
                # Show a message indicating successful deletion
                messagebox.showinfo("Success", "Transaction deleted successfully.")
                # Refresh the table
                self.populate_table()
            else:
                messagebox.showerror("Error", "Please select a transaction to delete.")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting transaction: {e}")
    
    def update_transaction(self):
        try:
            # Get selected item from the table
            selected_item = self.transactions_tree.selection()
            if selected_item:
                # Get transaction ID from the selected item
                transaction_id = self.transactions_tree.item(selected_item, "values")[4]
                
                # Get data from input fields
                type_value = self.type_var.get()
                category_value = self.category_var.get()
                amount_value_str = self.amount_entry.get()
                date_value = self.date_picker.get_date()
                
             
                # Validate amount
                if not amount_value_str:
                    raise ValueError("Amount cannot be empty.")
                amount_value = float(amount_value_str)
                
                # Format date
                formatted_date = datetime.strptime(date_value, "%m/%d/%y").strftime("%d/%m/%y")
                
                # Update the transaction in MongoDB
                self.collection.update_one({"_id": ObjectId(transaction_id)},
                                            {"$set": {"Type": type_value, "Category": category_value, 
                                                      "Date": formatted_date, "Amount": amount_value}})
                
                # Show a message indicating successful update
                messagebox.showinfo("Success", "Transaction updated successfully.")
                # Refresh the table
                self.populate_table()
            else:
                messagebox.showerror("Error", "Please select a transaction to update.")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating transaction: {e}")
    
    def on_double_click(self, event):
        # Get selected item from the table
        selected_item = self.transactions_tree.selection()
        if selected_item:
            # Populate the fields with the selected transaction's data
            self.type_var.set(self.transactions_tree.item(selected_item, "values")[0])
            self.category_var.set(self.transactions_tree.item(selected_item, "values")[1])
            self.date_picker.set_date(self.transactions_tree.item(selected_item, "values")[2])
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, self.transactions_tree.item(selected_item, "values")[3])
        else:
            messagebox.showerror("Error", "Please select a transaction to update.")
    
    def open_report_page(self):
        # Function to open the report page
        root = tk.Toplevel()  # Open report page in a new window
        report_page = ReportPage(root)
        root.mainloop()

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()