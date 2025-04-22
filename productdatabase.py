import sqlite3

conn = sqlite3.connect('products.db')
c = conn.cursor()

def create_product_table(product_name):
    table_name = f"{product_name.replace(' ', '_')}"
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            item_name TEXT,
            quantity INTEGER
        )
    """)  
    conn.commit()

def add_product_item(product_name, item_name, quantity):
    table_name = f"{product_name.replace(' ', '_')}"
    c.execute(f"""
        INSERT INTO {table_name} (item_name, quantity) VALUES (?, ?)
    """, (item_name, quantity))
    conn.commit()

def get_all_items(product_name):
    table_name = f"{product_name.replace(' ', '_')}"
    c.execute(f"SELECT item_name, quantity FROM {table_name}")
    return c.fetchall()

def get_all_product_names():
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table[0] for table in c.fetchall() if table]

def clear_product_table(product_name):
    table_name = f"{product_name.replace(' ', '_')}"
    c.execute(f"DELETE FROM {table_name};")
    conn.commit()
