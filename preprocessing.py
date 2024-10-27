import psycopg2


def set_planner_options(cursor, options):
    """Applies the specified planner settings for query optimization."""
    for option, state in options.items():
        cursor.execute(f"SET {option} = {'ON' if state else 'OFF'};")
    print("Planner options set successfully")


def reset_planner_options(cursor):
    """Resets all planner options to their default values."""
    cursor.execute("RESET enable_seqscan;")
    cursor.execute("RESET enable_indexscan;")
    cursor.execute("RESET enable_hashjoin;")
    cursor.execute("RESET enable_mergejoin;")
    print("Planner options reset successfully")



def run_query_with_settings(db_manager, query, settings):
    """Runs a query with specific planner settings and prints the execution plan."""
    set_planner_options(db_manager.cursor, settings)
    try:
        db_manager.cursor.execute(f"EXPLAIN ANALYZE {query}")
        plan = db_manager.cursor.fetchall()
        print("Execution Plan:")
        for line in plan:
            print(line)
    except Exception as e:
        print(f"Failed to execute query: {e}")
    finally:
        reset_planner_options(db_manager.cursor)

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
