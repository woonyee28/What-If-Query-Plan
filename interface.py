import streamlit as st
import pandas as pd
from preprocessing import connect_to_db, visualize_plan, printing_API_output, printing_steps_output
from whatif import get_qep, get_aqp

# Set the page configuration
st.set_page_config(page_title="Query Plan Visualizer", layout="wide")

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "dbname" not in st.session_state:
    st.session_state.dbname = ""
if "connection" not in st.session_state:
    st.session_state.connection = None
if "qep_plan" not in st.session_state:
    st.session_state.qep_plan = None
if "aqp_plan" not in st.session_state:
    st.session_state.aqp_plan = None
if "qep_cost" not in st.session_state:
    st.session_state.qep_cost = None
if "aqp_cost" not in st.session_state:
    st.session_state.aqp_cost = None

# Display login form if not logged in
if not st.session_state.logged_in:
    st.title("Welcome to the Query Plan Visualizer")
    st.markdown("""
    ### Project Summary: What-If Analysis of Query Plans

    The **What-If Analysis of Query Plans** project aims to develop a software tool that enables users to analyze and modify query execution plans (QEPs) for SQL queries. The project is a part of the **CX4031/SC3020 Database System Principles** course.

    ##### Key Objectives:
    1. **Visualize QEPs:** Display the query execution plans for given SQL queries.
    2. **What-If Scenarios:** Allow users to modify QEPs interactively and generate alternative query plans.
    3. **Cost Comparison:** Compare the estimated costs between the original QEP and modified AQP.
                 
    **Our Advisor:** Assoc Prof Sourav Saha Bhowmick

    **Team Members:**
    1. Ng Woon Yee
    2. Yang Yichen
    3. Tay Zhi Xian
    4. Alex Khoo Shien How
    5. Chua Ming Ru
    """)


    
    if st.button("Enter"):
        connection = connect_to_db()
        if connection:
            st.session_state.logged_in = True
            st.session_state.connection = connection
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Failed to connect. Check your credentials.")
else:
    # Main interface
    st.sidebar.header("Database schema (current DB: TPCH)")
    if st.sidebar.button("Exit"):
        st.session_state.logged_in = False
        st.session_state.connection = None
        # Clear stored plans and costs
        st.session_state.qep_plan = None
        st.session_state.aqp_plan = None
        st.session_state.qep_cost = None
        st.session_state.aqp_cost = None
        st.rerun()

    # Schema example display (static for now)
    schema_example = """
    - customer
    - lineitem
    - nation
    - orders
    - part
    - partsupp
    - region
    - supplier
    """
    st.sidebar.text(schema_example)

    st.sidebar.subheader("Example Queries")
    examples = [
        ("Query 1", """
        SELECT l_orderkey, SUM(l_extendedprice * (1 - l_discount)) AS revenue,
               o_orderdate, o_shippriority
        FROM customer, orders, lineitem
        WHERE c_mktsegment = 'HOUSEHOLD'
          AND c_custkey = o_custkey
          AND l_orderkey = o_orderkey
          AND o_orderdate < DATE '1995-03-21'
          AND l_shipdate > DATE '1995-03-21'
        GROUP BY l_orderkey, o_orderdate, o_shippriority
        ORDER BY revenue DESC, o_orderdate
        LIMIT 10;
        """),
        ("Query 2", """
        SELECT o_orderpriority, COUNT(*) AS order_count
        FROM orders
        WHERE o_orderdate >= DATE '1996-03-01'
          AND o_orderdate < DATE '1996-03-01' + INTERVAL '3' MONTH
          AND EXISTS (
            SELECT *
            FROM lineitem
            WHERE l_orderkey = o_orderkey
              AND l_commitdate < l_receiptdate
          )
        GROUP BY o_orderpriority
        ORDER BY o_orderpriority
        LIMIT 1;
        """),
        ("Query 3", """
        SELECT l_returnflag, l_linestatus,
               SUM(l_quantity) AS sum_qty,
               SUM(l_extendedprice) AS sum_base_price,
               SUM(l_extendedprice * (1 - l_discount)) AS sum_disc_price,
               SUM(l_extendedprice * (1 - l_discount) * (1 + l_tax)) AS sum_charge,
               AVG(l_quantity) AS avg_qty,
               AVG(l_extendedprice) AS avg_price,
               AVG(l_discount) AS avg_disc,
               COUNT(*) AS count_order
        FROM lineitem
        WHERE l_extendedprice > 100
        GROUP BY l_returnflag, l_linestatus
        ORDER BY l_returnflag, l_linestatus;
        """)
    ]

    example_names = [name for name, query in examples]
    selected_example_name = st.sidebar.radio("Select an example to load", example_names)
    selected_query = next(query for name, query in examples if name == selected_example_name)
    sql_query = st.text_area("SQL Query", selected_query.strip())

    # Run Query Button (Optional)
    if st.button("Run Query"):
        if st.session_state.connection:
            try:
                with st.session_state.connection.cursor() as cursor:
                    cursor.execute(sql_query)
                    results = cursor.fetchall()
                    colnames = [desc[0] for desc in cursor.description]
                    df = pd.DataFrame(results, columns=colnames)
                    st.subheader("Query Results")
                    st.dataframe(df)
            except Exception as e:
                st.error(f"Error executing query: {e}")
        else:
            st.error("No database connection available.")

    st.subheader("Modify Planner Methods (What-if Scenarios)")
    scan_methods = {
        "Sequential Scan": "enable_seqscan",
        "Index Scan": "enable_indexscan",
        "Bitmap Scan": "enable_bitmapscan",
        "TID Scan": "enable_tidscan"
    }

    join_methods = {
        "Nested Loop Join": "enable_nestloop",
        "Merge Join": "enable_mergejoin",
        "Hash Join": "enable_hashjoin"
    }

    # Display Scan Methods and Join Methods side by side
    col_scan, col_join = st.columns(2)

    with col_scan:
        st.write("**Scan Methods:**")
        selected_scans = {}
        for name, param in scan_methods.items():
            selected_scans[param] = st.checkbox(name, value=True)

    with col_join:
        st.write("**Join Methods:**")
        selected_joins = {}
        for name, param in join_methods.items():
            selected_joins[param] = st.checkbox(name, value=True)

    # Buttons to get QEP and AQP
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Get QEP"):
            if st.session_state.connection:
                get_qep(st.session_state.connection, sql_query)
            else:
                st.error("No database connection available.")

    with col2:
        if st.button("Get AQP"):
            if st.session_state.connection:
                scan_settings = {param: value for param, value in selected_scans.items()}
                join_settings = {param: value for param, value in selected_joins.items()}
                get_aqp(st.session_state.connection, sql_query, scan_settings, join_settings)
            else:
                st.error("No database connection available.")

    # Display plans outside of button conditions
    st.subheader("Query Plans")

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.qep_plan:
            st.write(f"**Query Execution Plan (QEP) - Total Cost: {st.session_state.qep_cost}**")
            visualize_plan(st.session_state.qep_plan)
        else:
            st.info("No QEP available. Click 'Get QEP' to retrieve it.")

    with col2:
        if st.session_state.aqp_plan:
            st.write(f"**Alternative Query Plan (AQP) - Total Cost: {st.session_state.aqp_cost}**")
            visualize_plan(st.session_state.aqp_plan)
        else:
            st.info("No AQP available. Click 'Get AQP' to retrieve it.")

    # Display cost comparison
    if st.session_state.qep_cost is not None and st.session_state.aqp_cost is not None:
        st.subheader("Cost Comparison")
        qep_cost = st.session_state.qep_cost
        aqp_cost = st.session_state.aqp_cost
        st.write(f"**QEP Total Cost:** {qep_cost}")
        st.write(f"**AQP Total Cost:** {aqp_cost}")
        cost_difference = aqp_cost - qep_cost
        st.write(f"**Cost Difference (AQP - QEP):** {cost_difference}")


    st.markdown("---")    
    st.markdown(
    "<u><b style='font-size: 30px;'>Natural Language Text Description for QEP</b></u>",
    unsafe_allow_html=True
    )
    if st.session_state.qep_plan:
        st.markdown("---")
        st.subheader("**SQL Steps Description**")
        reversed_steps = printing_steps_output(st.session_state.qep_plan)
        st.write("The query is executed as follows")
        for step in reversed_steps:
            st.write(step)

        st.markdown("---")
        st.subheader("**Natural Language Model Description**")
        NLM_description = printing_API_output(st.session_state.qep_plan)
        st.write(NLM_description)
        
    st.markdown("---")
    st.markdown(
    "<u><b style='font-size: 30px;'>Natural Language Text Description for AQP</b></u>",
    unsafe_allow_html=True
    )
    if st.session_state.aqp_plan:
        st.markdown("---")
        st.subheader("**SQL Steps Description for AQP:**")
        reversed_steps = printing_steps_output(st.session_state.aqp_plan)
        st.write("The query is executed as follows")
        for step in reversed_steps:
            st.write(step)

        st.markdown("---")
        st.subheader("**Natural Language Model Description for AQP:**")
        NLM_description = printing_API_output(st.session_state.aqp_plan)
        st.write(NLM_description)

    st.markdown("---")    

    if st.session_state.qep_plan:
        st.markdown(
        "<u><b style='font-size: 30px;'>Natural Language Model Description for Query</b></u>",
        unsafe_allow_html=True
        )
        query_description = printing_API_output(sql_query)
        st.write(query_description)