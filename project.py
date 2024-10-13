# project.py

import preprocessing
import interface

def main():
    # Load sample QEP from a file
    qep_data = preprocessing.load_qep_from_file("sample_qep.txt")
    
    # Run the GUI interface with loaded QEP data
    interface.run_interface(qep_data)

if __name__ == "__main__":
    main()