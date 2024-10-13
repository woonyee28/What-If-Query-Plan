# whatif.py

import subprocess

def generate_modified_sql(join_type):
    # Generate SQL query with modified join type
    sql_query = "SELECT * FROM table_a a JOIN table_b b ON a.id = b.id"
    if join_type == "Merge Join":
        modified_sql = f"SET enable_hashjoin = off; SET enable_mergejoin = on; {sql_query};"
    elif join_type == "Hash Join":
        modified_sql = f"SET enable_mergejoin = off; SET enable_hashjoin = on; {sql_query};"
    return modified_sql

def get_aqp_cost(sql_query):
    # Execute modified SQL query with EXPLAIN ANALYZE
    result = subprocess.run(['psql', '-c', f"EXPLAIN ANALYZE {sql_query}"], capture_output=True, text=True)
    return parse_cost(result.stdout)

def parse_cost(explain_output):
    # Extract cost estimate from EXPLAIN ANALYZE output
    lines = explain_output.splitlines()
    cost_line = lines[0] if lines else "cost=0.00..0.00"
    cost = cost_line.split('..')[-1].split(' ')[0]
    return float(cost) if cost.isdigit() else 0.0
