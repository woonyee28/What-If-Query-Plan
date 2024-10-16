# What-If-Query-Plan

## Data Source:
- TPC-H Tools Version: 3.0.1

## Instructions
```
pip install poetry
poetry install              # Install dependencies and create the virtual environment
poetry shell                # Activate the virtual environment
poetry add <package_name>   # To add new dependency
exit                        # To exit the virtual environment
```

## Meeting 15 Oct 2024:
1. Task Distribution
- Write code using psycopg2 to connect to PostgreSQL (Woon Yee)
- QEP Interface, Either using tkinter or Streamlit (Preferably)
 - Handle Changes in Algorithm, SQL Query Plan, Visualize Plan (Andrew)
 - Show Explanation and Total Cost (Ming Ru)
- WhatIf.py file, able to handle the changing of AQP <-> QEP
 - Handling the Changes in Algorithm (Text Replacing - Seq Scan <=> Index Scan, Hash Join <=> Merge Sort etc) (Yi Chen, Alex)
 - Compute the Cost the reflect the comparisons (Yi Chen, Alex)

## References:
- https://github.com/search?q=repo%3AVeeraraghavan-S-Nithyasri%2FSC3020_Query_P-Q%20psycopg2&type=code

## Example:
https://howardlee.cn/mocha/
https://howardlee.cn/lantern/
