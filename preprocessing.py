# preprocessing.py

# preprocessing.py

def parse_qep_output(qep_output):
    # Parse QEP into a structured format for visualization
    print("Parsing...")
    qep_data = []
    for line in qep_output.splitlines():
        node = {}
        parts = line.split()
        
        # Check if line contains "cost=" and parse cost information
        if 'cost=' in line:
            try:
                # Find the cost portion and parse it
                cost_part = line.split('cost=')[1].split('..')[-1].split(' ')[0]
                node['cost'] = float(cost_part)
            except (IndexError, ValueError):
                node['cost'] = 0.0  # Default to 0 if parsing fails

            # Set the operation type (e.g., Seq Scan, Nested Loop)
            node['operation'] = parts[0] if parts else "Unknown Operation"
        else:
            node['operation'] = parts[0] if parts else "Unknown Operation"
            node['cost'] = 0.0  # Set cost to 0 if not found
        
        qep_data.append(node)
    return qep_data

def load_qep_from_file(file_path):
    # Load QEP from a file and parse it
    with open(file_path, 'r') as file:
        qep_output = file.read()
    return parse_qep_output(qep_output)
