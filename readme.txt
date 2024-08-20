Overview

Expense Tracker is a desktop application developed using Python's Tkinter library. It allows users to track their income, expenses, and savings, providing detailed reports to help manage personal finances effectively.
Features

    User Authentication: Users can sign up, log in, and manage their accounts securely.
    Expense Tracking: Users can record their income, expenses, and savings with categories and dates.
    Detailed Reports: Generate reports for total income, expenses, and savings, as well as detailed yearly, monthly, and category-wise breakdowns.
    Data Visualization: Provides visual insights through graphs and charts to better understand financial data.
    Dark and Light Mode: Toggle between dark and light modes for a better user experience.

Installation
Prerequisites

    Python 3.x
    MongoDB
    Required Python packages: tkinter, pymongo, tkcalendar, matplotlib, pandas

Setup

    Clone the repository to your local machine.
    Install the required Python packages using pip:

    bash

pip install pymongo tkcalendar matplotlib pandas

Ensure MongoDB is running on your local machine.
Run the loginpage.py file to start the application:

bash

    python loginpage.py

File Structure

    loginpage.py: Handles user login and navigation to registration and main application pages.
    reg.py: Manages user registration, storing user credentials in MongoDB.
    exp.py: Core of the application, where users can input and track their financial data.
    report.py: Generates and displays various financial reports based on the tracked data.

Usage

    Login: Start by logging into the application with your credentials. If you are a new user, click on "New User?" to register.
    Add Income/Expense: After logging in, you can add your income, expenses, and savings by selecting the appropriate category, entering the amount, and selecting the date.
    View Reports: Navigate to the report section to generate and view various financial reports, such as total, yearly, monthly, and category-wise reports.
    Toggle Mode: Use the toggle option to switch between dark and light modes based on your preference.

Contributing

Contributions are welcome! Please create a pull request with a detailed description of the changes.