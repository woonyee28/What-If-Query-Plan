# preprocessing.py

import psycopg2
import streamlit as st
import networkx as nx
from pyvis.network import Network

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
