def parse_qep_output(qep_output):
    # Parse QEP to structured format (e.g., list of dictionaries for tree view)
    qep_data = []
    for line in qep_output.splitlines():
        node = {}
        # Simplified parsing; implement detailed parsing based on QEP output format
        node['operation'] = line.split()[0]
        node['cost'] = float(line.split('..')[-1].split(' ')[0])
        qep_data.append(node)
    return qep_data

def load_qep_from_file(file_path):
    # Load QEP from a file for testing and preprocessing
    with open(file_path, 'r') as file:
        qep_output = file.read()
    return parse_qep_output(qep_output)