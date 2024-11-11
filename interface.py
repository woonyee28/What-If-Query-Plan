import streamlit as st
import pandas as pd
from preprocessing import connect_to_db, visualize_plan, printing_API_output_query, printing_API_output_plan, printing_steps_output
from whatif import get_qep, get_aqp
from dbmanager import DatabaseManager

# Set the page configuration
st.set_page_config(page_title="Query Plan Visualizer", layout="wide")

# Initialize session state variables
if "welcome_complete" not in st.session_state:
    st.session_state.welcome_complete = False
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
if "db_location" not in st.session_state:
    st.session_state.db_location = None
if "csv_path" not in st.session_state:
    csv_path = "./datasets"
if "db_params" not in st.session_state:
    db_params = None
# To allow the last output to be stored in session state
if "last_aqp_plan" not in st.session_state:
    st.session_state.last_aqp_plan = None
    st.session_state.last_aqp_cached_steps = []
    st.session_state.last_plan_description = ""
if "last_qep_plan" not in st.session_state:
    st.session_state.last_qep_plan = None        
    st.session_state.last_qep_cached_steps = []
if "last_query" not in st.session_state:
    st.session_state.last_query_description = ""
    st.session_state.last_query = None      
    # Initialize session state for the toggle button
if "show_descriptions" not in st.session_state:
    st.session_state.show_descriptions = False


# Display login form if not logged in
if not st.session_state.get("welcome_complete"):
    # Title Section with icon
    st.title("🚀 Welcome to the Query Plan Visualizer")

    # Project Summary in a colored box
    st.markdown("""
    <div style="background-color: #141420; padding: 10px; border-radius: 10px;">
        <h3 style="color: #4b4b9f; text-align: center;">Project Summary: What-If Analysis of Query Plans</h3>
        <p>The <b>What-If Analysis of Query Plans</b> project aims to develop a software tool that enables users to analyze and modify query execution plans (QEPs) for SQL queries. This project is a part of the <b>SC3020 Database System Principles</b> course.</p>
    </div>
    """, unsafe_allow_html=True)

    # Key Objectives section with emojis for visual appeal
    st.markdown("""
    ### 🎯 Key Objectives:
    1. **Visualize QEPs**: Display the query execution plans for given SQL queries.
    2. **What-If Scenarios**: Allow users to modify QEPs interactively and generate alternative query plans.
    3. **Cost Comparison**: Compare the estimated costs between the original QEP and modified AQP.
    """)

    # Advisor and Team Members section with a horizontal line and different colors
    st.markdown("---")
    st.markdown("""
    <h4 style="color: #4b4b9f;">Our Advisor:</h4>
    <ul><li>Assoc Prof Sourav Saha Bhowmick</li></ul>
    
    <h4 style="color: #4b4b9f;">Team Members:</h4>
    <ul>
        <li>Ng Woon Yee</li>
        <li>Yang Yichen</li>
        <li>Tay Zhi Xian</li>
        <li>Alex Khoo Shien How</li>
        <li>Chua Ming Ru</li>
    </ul>
    """, unsafe_allow_html=True)

    # Enter button with custom styling
    if st.button("👉 Enter the Visualizer"):
        st.session_state.welcome_complete = True
        st.rerun()

    # Show login options if welcome is complete and not logged in
elif not st.session_state.logged_in:
    st.header("Database Login")

    # Choose between Local and Cloud database
    st.subheader("Choose Database Location")
    st.session_state.db_location = st.radio("Select Database Location", ("Cloud", "Local"))

    # Parameters for cloud database
    if st.session_state.db_location == "Cloud":
        if st.button("Log In"):
            db_params = {
                    'dbname': 'defaultdb',
                    'user': 'avnadmin',
                    'password': 'AVNS_mHAKcYWuEuMGRcuQcVi',
                    'host': 'sc3020-woonyee28.e.aivencloud.com',
                    'port': '14534',
                    'sslmode': 'require'
                }
            db_manager = DatabaseManager(db_params, csv_path)
            db_manager.connect()
            if db_manager.conn:
                    with db_manager.conn.cursor() as cursor:
                        cursor.execute("SET max_parallel_workers_per_gather = 0;")
                    db_manager.conn.commit()
                    st.session_state.logged_in = True
                    st.session_state.connection = db_manager.conn
                    st.success("Login successful!")
                    st.rerun()
            else:
                st.error("Failed to connect to the database.")
        
    elif st.session_state.db_location == "Local":
        # Obtain db_params for local database
        st.text("Enter local database credentials")
        dbname = st.text_input("Database Name", placeholder="Enter database name")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        host = st.text_input("Host", placeholder="e.g., localhost or IP address")
        port = st.text_input("Port",  placeholder="e.g., 5432")
        if st.button("Log In"):
            db_params = {
                "user": username,
                "password": password,
                "dbname": dbname,
                'host': host,
                'port': port,
                'sslmode': 'prefer'
            }
            try:
                db_manager = DatabaseManager(db_params, csv_path)
                db_manager.connect()
                # If the connection is successful, update the session state
                if db_manager.conn:
                    with db_manager.conn.cursor() as cursor:
                        cursor.execute("SET max_parallel_workers_per_gather = 0;")
                        cursor.execute("SET max_worker_processes = 1;")
                    db_manager.conn.commit()
                    st.session_state.logged_in = True
                    st.session_state.connection = db_manager.conn
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Failed to connect to the database.")
            except Exception as e:
                # Handle any connection errors and display an error message
                st.error(f"Failed to connect. Please check your credentials and try again. Error: {e}")

    # Exit button to go back to welcome screen
    if st.button("Exit"):
        st.session_state.welcome_complete = False
        st.rerun()

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
    if st.session_state.db_location == "Cloud":
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

    st.markdown("---")
    # Display cost comparison in two main columns
    main_col1, main_col2 = st.columns([1, 2])  # Left column for costs, right column for explanation

    # Left Column: Stack QEP, AQP, and Cost Difference vertically
    with main_col1:
        if st.session_state.qep_plan and st.session_state.aqp_plan:
            st.subheader("Cost Summary")
            
            # Display QEP Cost
            qep_cost = st.session_state.qep_cost
            st.write(f"**QEP Total Cost:** {qep_cost}")
            
            # Display AQP Cost
            aqp_cost = st.session_state.aqp_cost
            st.write(f"**AQP Total Cost:** {aqp_cost}")
            
            # Display Cost Difference
            cost_difference = aqp_cost - qep_cost
            st.write(f"**Cost Difference (AQP - QEP):** {cost_difference}")

    # Right Column: Cost Explanation
    with main_col2:
        if st.session_state.qep_plan and st.session_state.aqp_plan:
            st.subheader("Cost Explanation: AQP vs QEP")
            if (
                "last_plan_description" not in st.session_state
                or st.session_state.last_plan_description is None
                or st.session_state.last_qep_plan != st.session_state.qep_plan
                or st.session_state.last_aqp_plan != st.session_state.aqp_plan
            ):
                # Update only if the QEP or AQP plan has changed
                st.session_state.last_plan_description = printing_API_output_plan(
                    st.session_state.qep_plan, st.session_state.aqp_plan
                )
                st.session_state.last_qep_plan = st.session_state.qep_plan
                st.session_state.last_aqp_plan = st.session_state.aqp_plan
            st.markdown(f"""
                <div style="background-color:#322f3d; padding:15px; border-radius:5px;">
                    <p style="font-size: 16px; color:#ffffff;">{st.session_state.last_plan_description}</p>
                </div>
            """, unsafe_allow_html=True)
    if st.session_state.qep_plan and st.session_state.aqp_plan:    
        st.markdown("---")

    # Define a function to toggle the show_descriptions variable
    def toggle_descriptions():
        st.session_state.show_descriptions = not st.session_state.show_descriptions

    # Toggle button with callback to toggle descriptions
    st.button(
        "Hide QEP and AQP Descriptions" if st.session_state.show_descriptions else "Show QEP and AQP Descriptions",
        on_click=toggle_descriptions
    )

    # Display descriptions only if toggled to show
    if st.session_state.show_descriptions:
        # Display the descriptions in two columns side by side
        col1, col2 = st.columns(2)

        # QEP Description
        with col1:
            st.markdown(
                "<u><b style='font-size: 24px;'>Natural Language Description for QEP</b></u>",
                unsafe_allow_html=True
            )
            if st.session_state.qep_plan:
                st.session_state.last_qep_cached_steps = printing_steps_output(st.session_state.qep_plan)
                st.session_state.last_qep_plan = st.session_state.qep_plan

                # Build the HTML content for QEP steps in a gray box
                qep_steps_html = "<div style='background-color: #322f3d; padding: 15px; border-radius: 5px;'>"
                qep_steps_html += "<b>The query is executed as follows:</b><br><br>"
                for step in st.session_state.last_qep_cached_steps:
                    qep_steps_html += f"{step}<br><br>"
                qep_steps_html += "</div>"
                
                # Display QEP steps in a single markdown block
                st.markdown(qep_steps_html, unsafe_allow_html=True)
            else:
                st.info("No QEP available. Click 'Get QEP' to retrieve it.")

        # AQP Description
        with col2:
            st.markdown(
                "<u><b style='font-size: 24px;'>Natural Language Description for AQP</b></u>",
                unsafe_allow_html=True
            )
            if st.session_state.aqp_plan:
                # Update AQP steps in session state if plan is modified
                st.session_state.last_aqp_cached_steps = printing_steps_output(st.session_state.aqp_plan)
                st.session_state.last_aqp_plan = st.session_state.aqp_plan

                # Build the HTML content for AQP steps in a gray box
                aqp_steps_html = "<div style='background-color: #322f3d; padding: 15px; border-radius: 5px;'>"
                aqp_steps_html += "<b>The query is executed as follows:</b><br><br>"
                for step in st.session_state.last_aqp_cached_steps:
                    aqp_steps_html += f"{step}<br><br>"
                aqp_steps_html += "</div>"
                
                # Display AQP steps in a single markdown block
                st.markdown(aqp_steps_html, unsafe_allow_html=True)
            else:
                st.info("No AQP available. Click 'Get AQP' to retrieve it.")


    # # Display Query explanation separately
    # st.markdown("---")
    # st.markdown(
    #     "<u><b style='font-size: 24px;'>Natural Language Model Description for Query</b></u>",
    #     unsafe_allow_html=True
    # )
    # if st.session_state.last_query != sql_query:
    #     st.session_state.last_query_description = printing_API_output_query(sql_query)
    #     st.session_state.last_query = sql_query
    # st.write(st.session_state.last_query_description)


    # st.markdown("---")    
    # st.markdown(
    #     "<u><b style='font-size: 30px;'>Natural Language Model Description for Query</b></u>",
    #     unsafe_allow_html=True
    # )

    # # Display the LLM model otuput for quert explanation
    # if st.session_state.last_query != sql_query:
    #     st.session_state.last_query_description = printing_API_output_query(sql_query)
    #     st.session_state.last_query = sql_query
    # st.write(st.session_state.last_query_description)
