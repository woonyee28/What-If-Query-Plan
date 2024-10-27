# project.py

import preprocessing
import interface
from interface import get_user_options  # Assuming this function gets options based on GUI inputs
import psycopg2
from dbmanager import DatabaseManager
from psycopg2 import sql
import os



def main():
    db_params = {
        'dbname': 'your_db',
        'user': 'your_user',
        'password': 'your_password',
        'host': 'localhost',
        'port': '5432'
    }
    csv_path = "path_to_csv_files"

    # Instantiate DatabaseManager
    db_manager = DatabaseManager(db_params, csv_path)
    db_manager.connect()

    # Get options based on user input
    options = get_user_options()  # Retrieve user-selected planner settings

    # Run the query with the specific planner settings
    query = "SELECT * FROM your_table LIMIT 5;"
    preprocessing.run_query_with_settings(db_manager, query, settings)

    # Close the connection after use
    db_manager.close()
 

if __name__ == "__main__":
    main()