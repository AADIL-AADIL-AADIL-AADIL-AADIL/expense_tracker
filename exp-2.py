import json, os, datetime, tkinter as tk
from tkinter import messagebox, ttk

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses_file, self.salary_file = "expenses.json", "salary.json"
        
        # Load data
        self.expenses = self.load_data(self.expenses_file, [])
        self.salary = self.load_data(self.salary_file, {})
        
        # Create tabs
        notebook = ttk.Notebook(root)
        salary_frame = ttk.Frame(notebook)
        expense_frame = ttk.Frame(notebook)
        notebook.add(salary_frame, text="Salary")
        notebook.add(expense_frame, text="Expenses")
        notebook.pack(expand=1, fill="both")
        
        # Salary tab
        ttk.Label(salary_frame, text="Salary Amount (₹):").grid(row=0, column=0, padx=5, pady=5)
        self.salary_amount = ttk.Entry(salary_frame)
        self.salary_amount.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(salary_frame, text="Save Salary", command=self.save_salary).grid(row=0, column=2, padx=5, pady=5)
        
        # Expense tab
        ttk.Label(expense_frame, text="Amount (₹):").grid(row=0, column=0, padx=5, pady=5)
        self.amount = ttk.Entry(expense_frame)
        self.amount.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(expense_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.category = ttk.Combobox(expense_frame, values=["Food", "Transport", "Entertainment", "Shopping", "Bills", "Other"])
        self.category.grid(row=1, column=1, padx=5, pady=5)
        self.category.current(0)
        
        ttk.Label(expense_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        self.description = ttk.Entry(expense_frame)
        self.description.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(expense_frame, text="Add Expense", command=self.add_expense).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(expense_frame, text="Summary", command=self.show_summary).grid(row=3, column=1, padx=5, pady=5)
    
    def load_data(self, file, default):
        if os.path.exists(file):
            with open(file, "r") as f:
                try: return json.load(f)
                except: return default
        return default
    
    def save_salary(self):
        try:
            amount = float(self.salary_amount.get())
            month = datetime.datetime.now().strftime("%Y-%m")
            self.salary[month] = amount
            with open(self.salary_file, "w") as f: json.dump(self.salary, f)
            messagebox.showinfo("Success", "Salary updated successfully!")
            self.salary_amount.delete(0, tk.END)
        except ValueError: messagebox.showerror("Error", "Please enter a valid amount")
    
    def add_expense(self):
        try:
            amount = float(self.amount.get())
            expense = {"date": datetime.datetime.now().strftime("%Y-%m-%d"), 
                      "amount": amount, "category": self.category.get(), "description": self.description.get()}
            self.expenses.append(expense)
            with open(self.expenses_file, "w") as f: json.dump(self.expenses, f)
            messagebox.showinfo("Success", "Expense added successfully!")
            self.amount.delete(0, tk.END)
            self.description.delete(0, tk.END)
        except ValueError: messagebox.showerror("Error", "Please enter a valid amount")
    
    def show_summary(self):
        monthly = {}
        for e in self.expenses:
            month = e["date"][:7]
            monthly[month] = monthly.get(month, 0) + e["amount"]
        summary = "Monthly Expenses:\n" + "\n".join([f"{m}: ₹{a}" for m, a in monthly.items()])
        if self.salary: summary += "\n\nSalary:\n" + "\n".join([f"{m}: ₹{a}" for m, a in self.salary.items()])
        messagebox.showinfo("Summary", summary)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()