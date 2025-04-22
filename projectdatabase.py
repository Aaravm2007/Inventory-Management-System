import sqlite3

conn = sqlite3.connect('projects.db')
c = conn.cursor()

def create_project_table(project_name):
    table_name = f"{project_name.replace(' ', '_')}"
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            item_name TEXT,
            quantity INTEGER
        )
    """)  
    conn.commit()

def add_project_item(project_name, item_name, quantity):
    table_name = f"{project_name.replace(' ', '_')}"
    c.execute(f"""
        INSERT INTO {table_name} (item_name, quantity) VALUES (?, ?)
    """, (item_name, quantity))
    conn.commit()

def get_all_project_items(project_name):
    table_name = f"{project_name.replace(' ', '_')}"
    c.execute(f"SELECT item_name, quantity FROM {table_name}")
    return c.fetchall()

def get_all_project_names():
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table[0] for table in c.fetchall() if table]

def clear_project_table(project_name):
    table_name = f"{project_name.replace(' ', '_')}"
    c.execute(f"DELETE FROM {table_name};")
    conn.commit()