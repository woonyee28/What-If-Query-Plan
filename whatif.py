# whatif.py

import streamlit as st

def get_qep(connection, query):
    try:
        with connection.cursor() as cursor:
            explain_query = f"EXPLAIN (FORMAT JSON) {query}"
            cursor.execute(explain_query)
            result = cursor.fetchone()[0][0]
            plan = result['Plan']
            total_cost = plan['Total Cost']
            # Store in session state
            st.session_state.qep_plan = plan
            st.session_state.qep_cost = total_cost
            return plan, total_cost
    except Exception as e:
        st.error(f"Error retrieving QEP: {e}")
        return None, None

def get_aqp(connection, query, scan_settings, join_settings):
    try:
        with connection.cursor() as cursor:
            # Set the planner settings
            for param, value in {**scan_settings, **join_settings}.items():
                cursor.execute(f"SET {param} TO {'on' if value else 'off'};")
            # Use EXPLAIN to get the alternative query plan in JSON format
            explain_query = f"EXPLAIN (FORMAT JSON) {query}"
            cursor.execute(explain_query)
            result = cursor.fetchone()[0][0]
            plan = result['Plan']
            total_cost = plan['Total Cost']
            # Reset only the planner settings we changed
            for param in {**scan_settings, **join_settings}.keys():
                cursor.execute(f"RESET {param};")
            # Store in session state
            st.session_state.aqp_plan = plan
            st.session_state.aqp_cost = total_cost
            return plan, total_cost
    except Exception as e:
        st.error(f"Error retrieving AQP: {e}")
        return None, None
