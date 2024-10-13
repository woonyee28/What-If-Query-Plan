# interface.py
import tkinter as tk
from tkinter import messagebox
import project

class QueryOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Query Optimizer")

        # Input SQL query section
        tk.Label(root, text="Enter SQL Query:").grid(row=0, column=0, sticky="w")
        self.sql_entry = tk.Text(root, height=5, width=50)
        self.sql_entry.grid(row=1, column=0, padx=10, pady=10)

        # Input what-if question section
        tk.Label(root, text="Enter What-If Questions:").grid(row=2, column=0, sticky="w")
        self.what_if_entry = tk.Text(root, height=5, width=50)
        self.what_if_entry.grid(row=3, column=0, padx=10, pady=10)

        # Button to execute the query optimizer
        tk.Button(root, text="Optimize Query", command=self.run_optimizer).grid(row=4, column=0, pady=10)

        # Output results section
        self.result_display = tk.Text(root, height=10, width=50)
        self.result_display.grid(row=5, column=0, padx=10, pady=10)

    def run_optimizer(self):
        sql_query = self.sql_entry.get("1.0", "end-1c")
        what_if_questions = self.what_if_entry.get("1.0", "end-1c").splitlines()

        if not sql_query or not what_if_questions:
            messagebox.showerror("Input Error", "Please enter both SQL query and What-If questions.")
            return

        output = project.run_optimization(sql_query, what_if_questions)
        self.result_display.delete("1.0", "end")
        self.result_display.insert("end", output)

if __name__ == "__main__":
    root = tk.Tk()
    app = QueryOptimizerApp(root)
    root.mainloop()
