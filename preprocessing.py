# preprocessing.py
import re

def parse_sql_query(sql_query):
    """
    Parses an SQL query and returns its components.
    """
    # Simplified regex-based parsing, replace with actual SQL parsing for complex queries
    return {
        "select": re.findall(r"SELECT (.+?) FROM", sql_query, re.IGNORECASE),
        "from": re.findall(r"FROM (.+?)( WHERE| JOIN|$)", sql_query, re.IGNORECASE),
        "where": re.findall(r"WHERE (.+)", sql_query, re.IGNORECASE)
    }

