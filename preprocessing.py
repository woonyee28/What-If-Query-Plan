# preprocessing.py

import psycopg2
import re
import streamlit as st
import networkx as nx
from pyvis.network import Network
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from groq import Groq

def connect_to_db():
    try:
        # connection = psycopg2.connect(
        #     dbname=dbname,
        #     user=username,
        #     password=password,
        #     host="localhost",  # Change if using a different host
        #     port="5432"        # Default port for PostgreSQL
        # )
        db_params = {
            'dbname': 'defaultdb',
            'user': 'avnadmin',
            'password': 'AVNS_mHAKcYWuEuMGRcuQcVi',
            'host': 'sc3020-woonyee28.e.aivencloud.com',
            'port': '14534',
            'sslmode': 'require'
        }
        connection = psycopg2.connect(**db_params)
        connection.autocommit = True  # Enable autocommit
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

def visualize_plan(plan):
    G = nx.DiGraph()

    def add_nodes_edges(node, parent_id=None):
        node_id = id(node)
        node_type = node['Node Type']
        # Include more details in the label
        node_label = f"{node_type}\nCost: {node['Total Cost']}"
        if 'Relation Name' in node:
            node_label += f"\nRelation: {node['Relation Name']}"
        if 'Index Name' in node:
            node_label += f"\nIndex: {node['Index Name']}"
        G.add_node(node_id, label=node_label)
        if parent_id:
            G.add_edge(parent_id, node_id)

        for child in node.get('Plans', []):
            add_nodes_edges(child, node_id)

    add_nodes_edges(plan)

    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)
    net.repulsion(node_distance=200, spring_length=200)
    net.save_graph("plan.html")
    with open("plan.html", 'r', encoding='utf-8') as f:
        html = f.read()
    st.components.v1.html(html, height=600, scrolling=True)

    printing_output(plan)



# ALEX - TODO: TO COMPLETE FOR OTHER JOINS

def parse_plan_with_tables(plan, step_number=1, steps=None, intermediate_table_num=1):
    if steps is None:
        steps = []
        
    node_type = plan.get("Node Type")
    if node_type == "Seq Scan":
        node_type = "Sequential Scan"
    
    details = f"Step {step_number}: Perform {node_type}"


    if node_type in ["Sequential Scan", "Bitmap Heap Scan", "Index Scan", "Index Only Scan", "Bitmap Index Scan", "Tid Scan", "Sample Scan"]:
        table_name = plan.get("Relation Name")
        filter_condition = plan.get("Filter")


        if filter_condition:
            cleaned_condition = re.sub(r'::[a-zA-Z]+', '', filter_condition)  
            details += f" on table '{table_name}' and filter on ({cleaned_condition}) "
        else:
            details += f" on table '{table_name}' "

    elif node_type == "Nested Loop":
        details += f" with nested join conditions "

    elif node_type == "Sort":
        sort_keys = ", ".join(plan.get("Sort Key", []))
        details += f", sorted by {sort_keys}."

    elif node_type == "Aggregate":
        strategy = plan.get("Strategy", "Unknown strategy")
        group_keys = ", ".join(plan.get("Group Key", []))
        details += f" using {strategy} strategy. Grouping on keys: {group_keys} "

    elif node_type == "Hash Join":
        hash_condition = plan.get("Hash Cond")
        tables = set([term.split('.')[0] for term in hash_condition.replace('(', '').replace(')', '').split(' = ')])
        details += f" using condition {hash_condition} to join tables {tables} "
    
    elif node_type == "Hash" and "Plans" in plan:
        details += " to prepare a hash table for efficient join operations "
        for sub_plan in plan["Plans"]:
            if "Relation Name" in sub_plan:
                relation_name = sub_plan["Relation Name"]
                details += f" The relation used to form the hash table is '{relation_name}' "

    elif node_type == "Limit":
        details += f" to limit results to {plan.get('Plan Rows', 'a specified number')} rows and get the final result "
    
    steps.append(details)

    if "Plans" in plan:
        for sub_plan in plan["Plans"]:
            step_number += 1
            intermediate_table_num += 1
            parse_plan_with_tables(sub_plan, step_number, steps, intermediate_table_num)
    
    return steps


def printing_output(plan):
    steps = parse_plan_with_tables(plan)
    total_steps = len(steps)
    reversed_steps = [
        f"Step {i+1}: {step[step.index(':')+1:].strip()} to get intermediate table T{i + 1}"
        for i, step in enumerate(steps[::-1])
    ]

    print("The query is executed as follows")
    # Print each step in the reversed parsed output
    for step in reversed_steps:
        print(step)
    return


def printing_API_output(query):
    client = Groq(api_key='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')

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Explain the query {query};",
            }
        ],
        model="llama3-8b-8192",
        stream=False,
    )

    print(chat_completion.choices[0].message.content)
