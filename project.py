
Copy code
# project.py

import interface
import preprocessing

def main():
    # Read sample QEP from a file for demo
    qep_data = preprocessing.load_qep_from_file("sample_qep.txt")

    # Initialize GUI with QEP data
    root = interface.tk.Tk()
    app = interface.QEPInterface(root)
    app.load_qep(qep_data)
    root.mainloop()

if __name__ == "__main__":
    main()