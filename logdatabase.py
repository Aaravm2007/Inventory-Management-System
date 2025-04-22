import sqlite3
from datetime import datetime
conn = sqlite3.connect('ims.db') #:memory:
c = conn.cursor()

'''c.execute ("""CREATE TABLE function_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            function_name TEXT,
            call_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_name text,
            description TEXT
            )""")
conn.commit()'''

def log_function_call(function_name,username,description):
    with conn:
        c.execute("INSERT INTO function_history (function_name, call_time,user_name,description) VALUES (?,?, ?,?)",
                  (function_name, datetime.now(),username,description))
        
def get_function_history():
    with conn:
        c.execute("SELECT * FROM function_history")
        return c.fetchall()