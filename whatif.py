# whatif.py
import sqlite3
from preprocessing import parse_sql_query

def generate_aqp(sql_query, what_if_modifications):
    """
    Generates a modified SQL query based on what-if questions
    and retrieves the corresponding AQP with cost estimation.
    """

    parsed_query = parse_sql_query(sql_query)
    modified_sql_query = apply_modifications(parsed_query, what_if_modifications)

    # Execute the query on a test database
    db_connection = sqlite3.connect(":memory:")
    setup_sample_database(db_connection)
    original_plan, original_cost = get_query_plan_cost(db_connection, sql_query)
    modified_plan, modified_cost = get_query_plan_cost(db_connection, modified_sql_query)
    
    db_connection.close()
    return {
        "original_sql": sql_query,
        "modified_sql": modified_sql_query,
        "original_plan": original_plan,
        "original_cost": original_cost,
        "modified_plan": modified_plan,
        "modified_cost": modified_cost
    }

def apply_modifications(parsed_query, modifications):
    """
    Applies modifications based on what-if scenarios to the parsed SQL query.
    """
    # Modify parsed_query based on modifications
    modified_query = "SELECT ... FROM ... WHERE ..."  # Constructed modified SQL query
    return modified_query

def get_query_plan_cost(db_connection, sql_query):
    """
    Retrieves the query plan and cost using EXPLAIN QUERY PLAN.
    """
    cursor = db_connection.cursor()
    try:
        # Debug: Print the SQL query to inspect its syntax before execution
        print("Executing EXPLAIN QUERY PLAN on:", sql_query)
        
        # Execute the EXPLAIN QUERY PLAN statement
        cursor.execute(f"EXPLAIN QUERY PLAN {sql_query}")
        
        # Fetch and interpret the query plan and cost estimation
        plan = cursor.fetchall()
        cost = sum(row[2] for row in plan) if plan else 0.0  # Assuming cost is in row[2]
        
        return plan, cost
    except sqlite3.OperationalError as e:
        print("OperationalError:", e)
        print("Error executing query:", sql_query)
        return None, None



def setup_sample_database(db_connection):
    """
    Sets up sample tables and data in the SQLite in-memory database.
    """
    cursor = db_connection.cursor()
    # Example: Creating an employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            department TEXT
        )
    """)

    # Insert sample data
    cursor.executemany("""
        INSERT INTO employees (name, age, department) VALUES (?, ?, ?)
    """, [
        ("Alice", 30, "HR"),
        ("Bob", 35, "Engineering"),
        ("Charlie", 28, "Marketing"),
    ])
    db_connection.commit()