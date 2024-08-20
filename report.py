import tkinter as tk
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

class ReportPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Report")
        
        # Connect to MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['expense_tracker']
        self.collection = self.db['expenses']
        
        # Load data from MongoDB into a DataFrame
        self.df = self.load_data_from_mongo()
        
        # Create buttons for generating reports
        self.create_buttons()

        # Text widget to display the reports
        self.report_text = tk.Text(self.root, height=20, width=60)
        self.report_text.pack()

    def load_data_from_mongo(self):
        # Fetch data from MongoDB collection
        data = list(self.collection.find())
        
        # Create DataFrame from the fetched data
        df = pd.DataFrame(data)
        
        # Convert Date column to datetime format
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
        return df

    def create_buttons(self):
        # Button to generate Total Income, Expense, and Saving Report
        total_report_button = tk.Button(self.root, text="Total Report", command=self.generate_total_report)
        total_report_button.pack(pady=10)

        # Button to generate Yearly Income, Expense, and Saving Report
        yearly_report_button = tk.Button(self.root, text="Yearly Report", command=self.generate_yearly_report)
        yearly_report_button.pack(pady=10)

        # Button to generate Category-wise Expense Report
        category_report_button = tk.Button(self.root, text="Category-wise Expense Report", command=self.generate_category_report)
        category_report_button.pack(pady=10)

        # Button to generate Month-wise Income Report
        monthly_report_button = tk.Button(self.root, text="Monthly Income Report", command=self.generate_monthly_report)
        monthly_report_button.pack(pady=10)

        # Button to generate Saving vs Expense Report
        saving_expense_report_button = tk.Button(self.root, text="Saving vs Expense Report", command=self.generate_saving_expense_report)
        saving_expense_report_button.pack(pady=10)

    def clear_report_text(self):
        # Clear the text widget
        self.report_text.delete('1.0', tk.END)

    def generate_total_report(self):
        # Clear previous report
        self.clear_report_text()

        # Calculate total income and expense
        total_income = self.df[self.df['Type'] == 'Income']['amount'].sum()
        total_expense = self.df[self.df['Type'] == 'Expense']['amount'].sum()
        total_saving = total_income - total_expense

        # Display the report in the text widget
        report = f"Total Income: {total_income}, Total Expense: {total_expense}, Total Saving: {total_saving}\n"
        self.report_text.insert(tk.END, report)

        # Create a bar graph
        labels = ['Income', 'Expense', 'Saving']
        values = [total_income, total_expense, total_saving]

        plt.figure(figsize=(8, 5))
        plt.bar(labels, values, color=['green', 'red', 'blue'])
        plt.title('Total Report')
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.show()

    def generate_yearly_report(self):
        # Clear previous report
        self.clear_report_text()

        # Calculate yearly income and expense
        self.df['Year'] = self.df['Date'].dt.year
        yearly_data = self.df.groupby(['Year', 'Type'])['amount'].sum().unstack(fill_value=0)
        yearly_data['Saving'] = yearly_data['Income'] - yearly_data['Expense']

        # Plotting multi-line graph for yearly report
        plt.figure(figsize=(10, 6))
        for col in yearly_data.columns:
            plt.plot(yearly_data.index, yearly_data[col], marker='o', label=col)

        plt.title('Yearly Report')
        plt.xlabel('Year')
        plt.ylabel('Amount')
        plt.legend()
        plt.grid(True)
        plt.show()

    def generate_category_report(self):
        # Clear previous report
        self.clear_report_text()

        # Calculate total expense for each category
        category_expenses = self.df[self.df['Type'] == 'Expense'].groupby('Category')['amount'].sum()

        # Create labels and values for the pie chart
        labels = category_expenses.index.tolist()
        values = category_expenses.tolist()

        # Display the report in the text widget
        for category, total_expense in zip(labels, values):
            report = f"Category: {category}, Total Expense: {total_expense}\n"
            self.report_text.insert(tk.END, report)

        # Create a pie chart
        plt.figure(figsize=(8, 5))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Category-wise Expense Report')
        plt.show()

    def generate_monthly_report(self):
        # Clear previous report
        self.clear_report_text()

        # Calculate monthly income
        monthly_income = self.df[self.df['Type'] == 'Income'].groupby(pd.Grouper(key='Date', freq='M'))['amount'].sum()

        # Plotting line graph for monthly income
        plt.figure(figsize=(10, 6))
        for year, data in monthly_income.groupby(monthly_income.index.year):
            plt.plot(data.index.month, data.values, marker='o', label=year)

        plt.title('Monthly Income Report')
        plt.xlabel('Month')
        plt.ylabel('Income')
        plt.legend(title='Year')
        plt.grid(True)
        plt.show()
    def generate_saving_expense_report(self):
        # Clear previous report
        self.clear_report_text()

        # Calculate total income and expense
        total_income = self.df[self.df['Type'] == 'Income']['amount'].sum()
        total_expense = self.df[self.df['Type'] == 'Expense']['amount'].sum()
        total_saving = total_income - total_expense

        report = f"Total Expense: {total_expense}, Total Saving: {total_saving}\n"
        self.report_text.insert(tk.END, report)


# Main function for testing
if __name__ == "__main__":
    root = tk.Tk()
    report_page = ReportPage(root)
    root.mainloop()

