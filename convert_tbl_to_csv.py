import os

def convert_tbl_to_csv(tbl_file, csv_file):
    with open(tbl_file, 'r') as tbl, open(csv_file, 'w', newline='') as csv:
        for line in tbl:
            line = line.rstrip('|').strip()
            csv.write(line + '\n')

def convert_all_tbl_files(directory):
    tbl_files = [f for f in os.listdir(directory) if f.endswith('.tbl')]
    
    for tbl_file in tbl_files:
        csv_file = os.path.join(directory, tbl_file.replace('.tbl', '.csv'))
        
        convert_tbl_to_csv(os.path.join(directory, tbl_file), csv_file)
        print(f"Converted {tbl_file} to {csv_file}")

if __name__ == "__main__":
    directory = "./datasets"
    
    convert_all_tbl_files(directory)
