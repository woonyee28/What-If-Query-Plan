# interface.py

import tkinter as tk
from tkinter import ttk
import whatif
import preprocessing

class QEPInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("QEP What-If Analysis Tool")

        # Main Frame
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Tree View for QEP visualization
        self.tree = ttk.Treeview(self.frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Control Panel for "what-if" options
        self.control_frame = tk.Frame(self.frame)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Add Control options
        tk.Label(self.control_frame, text="Modify QEP Node").pack()
        self.join_type = tk.StringVar(value="Hash Join")
        tk.Radiobutton(self.control_frame, text="Hash Join", variable=self.join_type, value="Hash Join").pack()
        tk.Radiobutton(self.control_frame, text="Merge Join", variable=self.join_type, value="Merge Join").pack()
        
        tk.Button(self.control_frame, text="Apply What-If", command=self.apply_what_if).pack()

    def load_qep(self, qep_data):
        # Populate tree with QEP data (simplified example)
        for node in qep_data:
            self.tree.insert('', 'end', text=node['operation'], values=(node['cost']))

    def apply_what_if(self):
        selected_join = self.join_type.get()
        modified_sql = whatif.generate_modified_sql(selected_join)
        aqp_cost = whatif.get_aqp_cost(modified_sql)
        print(f"Modified SQL: {modified_sql}\nAQP Cost: {aqp_cost}")

def main():
    root = tk.Tk()
    app = QEPInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()