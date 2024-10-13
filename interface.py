# interface.py

import tkinter as tk
from tkinter import ttk
import whatif

class QEPInterface:
    def __init__(self, root, qep_data):
        self.root = root
        self.qep_data = qep_data
        self.root.title("QEP What-If Analysis Tool")

        # Main Frame
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Tree View for QEP visualization
        self.tree = ttk.Treeview(self.frame, columns=("Cost",), show="tree headings")
        self.tree.heading("#0", text="Operation")
        self.tree.heading("Cost", text="Cost")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Load initial QEP into the tree view
        self.load_qep()

        # Control Panel for "what-if" options
        self.control_frame = tk.Frame(self.frame)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Control options
        tk.Label(self.control_frame, text="Modify QEP Node").pack()
        self.join_type = tk.StringVar(value="Hash Join")
        tk.Radiobutton(self.control_frame, text="Hash Join", variable=self.join_type, value="Hash Join").pack()
        tk.Radiobutton(self.control_frame, text="Merge Join", variable=self.join_type, value="Merge Join").pack()
        tk.Button(self.control_frame, text="Apply What-If", command=self.apply_what_if).pack()

    def load_qep(self):
        # Populate tree with QEP data
        for node in self.qep_data:
            self.tree.insert('', 'end', text=node['operation'], values=(node['cost']))

    def apply_what_if(self):
        selected_join = self.join_type.get()
        modified_sql = whatif.generate_modified_sql(selected_join)
        aqp_cost = whatif.get_aqp_cost(modified_sql)
        print(f"Modified SQL: {modified_sql}\nAQP Cost: {aqp_cost}")

def run_interface(qep_data):
    root = tk.Tk()
    app = QEPInterface(root, qep_data)
    root.mainloop()