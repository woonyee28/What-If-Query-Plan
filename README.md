# What-If-Query-Plan

# PostgreSQL Version
- 17.0 Windows x86-64
- remember to add to PATH -> Eg: C:\Program Files\PostgreSQL\17\bin
- After path is added you can get something like this in cmd to initiate a session to verify that PostgreSQL is installed!
```
C:\Users\snorl>psql -U postgres
Password for user postgres:

psql (17.0)
WARNING: Console code page (437) differs from Windows code page (1252)
         8-bit characters might not work correctly. See psql reference
         page "Notes for Windows users" for details.
Type "help" for help.

postgres=# CREATE DATABASE sc3020;
CREATE DATABASE
```
- create a new database called sc3020!
- dbmanager.py
```
(what-if-query-plan-py3.10) C:\Users\snorl\Desktop\What-If-Query-Plan>python dbmanager.py
Database connection successful
All tables dropped successfully
Tables created successfully
Data loaded successfully into region
Data loaded successfully into nation
Data loaded successfully into customer
Data loaded successfully into supplier
Data loaded successfully into orders
Data loaded successfully into part
Data loaded successfully into partsupp
Data loaded successfully into lineitem

Executing a sample query:
(0, 'AFRICA                   ', 'lar deposits. blithely final packages cajole. regular waters are final requests. regular accounts are according to ')
(1, 'AMERICA                  ', 'hs use ironic, even requests. s')
(2, 'ASIA                     ', 'ges. thinly even pinto beans ca')
(3, 'EUROPE                   ', 'ly final courts cajole furiously final excuse')
(4, 'MIDDLE EAST              ', 'uickly special accounts cajole carefully blithely close requests. carefully final asymptotes haggle furiousl')
Database connection closed
```

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
 - Handling the Changes in Algorithm (Text Replacing - Seq Scan <=> Index Scan, Hash Join <=> Merge Sort etc) (Alex)
 - Compute the Cost the reflect the comparisons (Yi Chen)

## References:
- https://github.com/search?q=repo%3AVeeraraghavan-S-Nithyasri%2FSC3020_Query_P-Q%20psycopg2&type=code

## Example:
https://howardlee.cn/mocha/
https://howardlee.cn/lantern/

