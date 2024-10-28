import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Query Plan Visualizer", layout="wide")

# Create the layout
st.sidebar.header("Database schema (current DB: TPCH)")
# Simulating a schema explorer
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

# Examples section
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
      AND l_shipdate > DATE '1955-03-21'
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

# Create a list of example names for selection
example_names = [name for name, query in examples]
selected_example_name = st.sidebar.radio("Select an example to load", example_names)

# Find the SQL query based on the selected example name
selected_query = next(query for name, query in examples if name == selected_example_name)

# Pre-fill the SQL query when an example is selected
sql_query = st.text_area("SQL Query", selected_query.strip())

# Config Alternative Plans
st.subheader("Config Alternative Plans")

# Parameters and options
col1, col2 = st.columns(2)

with col1:
    max_config = st.number_input("Max config parameters", min_value=1, max_value=10, value=6)
    approach = st.selectbox("Select an approach", ["SINGLE plan (default)", "MULTIPLE plans", "CUSTOM"])

with col2:
    st.write("Select parameter(s):")
    params = ["Bitmap Scan", "Index Scan", "Index-Only Scan", "Sequential Scan",
              "TID Scan", "Hash Join", "Merge Join", "Nested-Loop Join",
              "Hashed Aggregation", "Sorted Aggregation", "Limit", "Materialize",
              "Sort"]
    selected_params = st.multiselect("", params)

# Visualization and explanation area
st.subheader("Visualize Plan")

# Dummy dropdown to simulate plan selection
plan_selection = st.selectbox("Choose one plan to view", ["Plan A", "Plan B", "Plan C"])

# Explanation and Total Cost
col3, col4 = st.columns(2)

with col3:
    st.subheader("Explanation")
    st.text_area("Explanation", "Explanation of why the QEP is selected for the input query by connecting its content with existing knowledge.", height=150)

with col4:
    st.subheader("Total Cost")
    st.text("Cost details will appear here.")

# Button for detailed view
if st.button("Detailed view"):
    st.write("Displaying detailed plan view... (to be implemented)")