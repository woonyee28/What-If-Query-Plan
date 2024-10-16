import psycopg2
from psycopg2 import sql
import os

class DatabaseManager:
    def __init__(self, db_params, csv_path):
        self.db_params = db_params
        self.csv_path = csv_path
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.db_params)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            print("Database connection successful")
        except Exception as e:
            print(f"Failed to connect to the database: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed")

    def drop_all_tables(self):
        """Drops all tables in the database."""
        try:
            drop_command = """
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
            """
            self.cursor.execute(drop_command)
            print("All tables dropped successfully")
        except Exception as e:
            print(f"Failed to drop tables: {e}")

    def create_tables(self):
        create_table_commands = [
            """
            CREATE TABLE IF NOT EXISTS public.region
            (
                r_regionkey integer NOT NULL,
                r_name character(25) COLLATE pg_catalog."default" NOT NULL,
                r_comment character varying(152) COLLATE pg_catalog."default",
                CONSTRAINT region_pkey PRIMARY KEY (r_regionkey)
            );
            
            ALTER TABLE public.region
                OWNER to postgres; 
            """,
            """
            CREATE TABLE IF NOT EXISTS public.nation (
                n_nationkey INTEGER NOT NULL,
                n_name CHARACTER(25) COLLATE pg_catalog."default" NOT NULL,
                n_regionkey INTEGER NOT NULL,
                n_comment CHARACTER VARYING(152) COLLATE pg_catalog."default",
                CONSTRAINT nation_pkey PRIMARY KEY (n_nationkey),
                CONSTRAINT fk_nation FOREIGN KEY (n_regionkey)
                    REFERENCES public.region (r_regionkey) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
            );
            
            ALTER TABLE public.nation
                OWNER to postgres; 
            """,
            """
            CREATE TABLE IF NOT EXISTS public.part (
                p_partkey INTEGER NOT NULL,
                p_name CHARACTER VARYING(55) COLLATE pg_catalog."default" NOT NULL,
                p_mfgr CHARACTER(25) COLLATE pg_catalog."default" NOT NULL,
                p_brand CHARACTER(10) COLLATE pg_catalog."default" NOT NULL,
                p_type CHARACTER VARYING(25) COLLATE pg_catalog."default" NOT NULL,
                p_size INTEGER NOT NULL,
                p_container CHARACTER(10) COLLATE pg_catalog."default" NOT NULL,
                p_retailprice NUMERIC(15, 2) NOT NULL,
                p_comment CHARACTER VARYING(23) COLLATE pg_catalog."default",
                CONSTRAINT part_pkey PRIMARY KEY (p_partkey)
            );
            
            ALTER TABLE public.part
                OWNER to postgres; 
            """,
            """
            CREATE TABLE IF NOT EXISTS public.supplier (
                s_suppkey INTEGER NOT NULL,
                s_name CHARACTER(25) COLLATE pg_catalog."default" NOT NULL,
                s_address CHARACTER VARYING(40) COLLATE pg_catalog."default" NOT NULL,
                s_nationkey INTEGER NOT NULL,
                s_phone CHARACTER(15) COLLATE pg_catalog."default" NOT NULL,
                s_acctbal NUMERIC(15, 2) NOT NULL,
                s_comment CHARACTER VARYING(101) COLLATE pg_catalog."default",
                CONSTRAINT supplier_pkey PRIMARY KEY (s_suppkey),
                CONSTRAINT fk_supplier FOREIGN KEY (s_nationkey)
                    REFERENCES public.nation (n_nationkey) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
            );
            
            ALTER TABLE public.supplier
                OWNER to postgres; 
            """,
            """
            CREATE TABLE IF NOT EXISTS public.partsupp (
                ps_partkey INTEGER NOT NULL,
                ps_suppkey INTEGER NOT NULL,
                ps_availqty INTEGER NOT NULL,
                ps_supplycost NUMERIC(15, 2) NOT NULL,
                ps_comment CHARACTER VARYING(199) COLLATE pg_catalog."default",
                CONSTRAINT partsupp_pkey PRIMARY KEY (ps_partkey, ps_suppkey),
                CONSTRAINT fk_ps_suppkey FOREIGN KEY (ps_suppkey)
                REFERENCES public.supplier (s_suppkey)
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
                CONSTRAINT fk_ps_partkey FOREIGN KEY (ps_partkey)
                    REFERENCES public.part (p_partkey) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
            );
            
            ALTER TABLE public.partsupp
                OWNER to postgres; 
            """,
            """
            CREATE TABLE IF NOT EXISTS public.customer (
                c_custkey INTEGER NOT NULL,
                c_name CHARACTER VARYING(25) COLLATE pg_catalog."default" NOT NULL,
                c_address CHARACTER VARYING(40) COLLATE pg_catalog."default" NOT NULL,
                c_nationkey INTEGER NOT NULL,
                c_phone CHARACTER(15) COLLATE pg_catalog."default" NOT NULL,
                c_acctbal NUMERIC(15, 2) NOT NULL,
                c_mktsegment CHARACTER(10) COLLATE pg_catalog."default" NOT NULL,
                c_comment CHARACTER VARYING(117) COLLATE pg_catalog."default",
                CONSTRAINT customer_pkey PRIMARY KEY (c_custkey),
                CONSTRAINT fk_customer FOREIGN KEY (c_nationkey)
                    REFERENCES public.nation (n_nationkey) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
            );
            
            ALTER TABLE public.customer
                OWNER to postgres; 
            """,
            """
            CREATE TABLE IF NOT EXISTS public.orders (
                o_orderkey INTEGER NOT NULL,
                o_custkey INTEGER NOT NULL,
                o_orderstatus CHARACTER(1) COLLATE pg_catalog."default" NOT NULL,
                o_totalprice NUMERIC(15, 2) NOT NULL,
                o_orderdate DATE NOT NULL,
                o_orderpriority CHARACTER(15) COLLATE pg_catalog."default" NOT NULL,
                o_clerk CHARACTER(15) COLLATE pg_catalog."default" NOT NULL,
                o_shippriority INTEGER NOT NULL,
                o_comment CHARACTER VARYING(79) COLLATE pg_catalog."default",
                CONSTRAINT orders_pkey PRIMARY KEY (o_orderkey),
                CONSTRAINT fk_orders FOREIGN KEY (o_custkey)
                    REFERENCES public.customer (c_custkey) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
            );
            
            ALTER TABLE public.orders
                OWNER to postgres; 
            """,
            """
            CREATE TABLE IF NOT EXISTS public.lineitem (
                l_orderkey INTEGER NOT NULL,
                l_partkey INTEGER NOT NULL,
                l_suppkey INTEGER NOT NULL,
                l_linenumber INTEGER NOT NULL,
                l_quantity DECIMAL(15, 2) NOT NULL,
                l_extendedprice DECIMAL(15, 2) NOT NULL,
                l_discount DECIMAL(15, 2) NOT NULL,
                l_tax DECIMAL(15, 2) NOT NULL,
                l_returnflag CHARACTER(1) NOT NULL,
                l_linestatus CHARACTER(1) NOT NULL,
                l_shipdate DATE NOT NULL,
                l_commitdate DATE NOT NULL,
                l_receiptdate DATE NOT NULL,
                l_shipinstruct CHARACTER(25) NOT NULL,
                l_shipmode CHARACTER(10) NOT NULL,
                l_comment CHARACTER VARYING(44) NOT NULL,
                CONSTRAINT lineitem_pkey PRIMARY KEY (l_orderkey, l_linenumber),
                CONSTRAINT fk_lineitem_order FOREIGN KEY (l_orderkey)
                    REFERENCES public.orders (o_orderkey) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION,
                CONSTRAINT fk_lineitem_part FOREIGN KEY (l_partkey)
                    REFERENCES public.part (p_partkey) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION,
                CONSTRAINT fk_lineitem_supp FOREIGN KEY (l_suppkey)
                    REFERENCES public.supplier (s_suppkey) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
            );
            ALTER TABLE public.lineitem
                OWNER to postgres; 
            """
        ]

        try:
            for command in create_table_commands:
                self.cursor.execute(command)
            print("Tables created successfully")
        except Exception as e:
            print(f"Failed to create tables: {e}")

    def load_csv_to_table(self, table_name, csv_file):
        try:
            with open(csv_file, 'r') as f:
                self.cursor.copy_expert(sql.SQL("""
                    COPY {} FROM STDIN WITH CSV DELIMITER '|' NULL '' 
                """).format(sql.Identifier(table_name)), f)
            print(f"Data loaded successfully into {table_name}")
        except Exception as e:
            print(f"Failed to load data into {table_name}: {e}")

    def load_all_csv(self):
        csv_files = {
            'region': os.path.join(self.csv_path, 'region.csv'),
            'nation': os.path.join(self.csv_path, 'nation.csv'),
            'customer': os.path.join(self.csv_path, 'customer.csv'),
            'supplier': os.path.join(self.csv_path, 'supplier.csv'),
            'orders': os.path.join(self.csv_path, 'orders.csv'),
            'part': os.path.join(self.csv_path, 'part.csv'),
            'partsupp': os.path.join(self.csv_path, 'partsupp.csv'),
            'lineitem': os.path.join(self.csv_path, 'lineitem.csv')
        }


        for table, csv_file in csv_files.items():
            self.load_csv_to_table(table, csv_file)

    def run_query(self, query):
        """Run a SQL query and print the results."""
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            for row in results:
                print(row)
        except Exception as e:
            print(f"Failed to execute query: {e}")


if __name__ == "__main__":
    db_params = {
        'dbname': 'sc3020',
        'user': 'postgres',
        'password': 'nopassword',
        'host': 'localhost',  
        'port': '5432'
    }

    csv_path = "C:/Users/snorl/Desktop/What-If-Query-Plan/datasets" 

    db_manager = DatabaseManager(db_params, csv_path)

    db_manager.connect()

    # db_manager.drop_all_tables()

    db_manager.create_tables()

    db_manager.load_all_csv()

    print("\nExecuting a sample query:")
    db_manager.run_query("SELECT * FROM public.region LIMIT 5;")

    # Close the database connection
    db_manager.close()

