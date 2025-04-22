import sqlite3

conn = sqlite3.connect('ims.db') #:memory:
c = conn.cursor()

'''c.execute ("""CREATE TABLE stock (
          id int,
          itemname text, 
          unit text,
          quantity int,
          minimumquantity int,
          moq int
          )""")
conn.commit()'''

def new_stock(id,itemname,unit,quantity,minimumquantity,moq):
    with conn:
        c.execute("INSERT INTO stock VALUES (:id,:itemname,:unit,:quantity,:minimumquantity,:moq)",
        {'id':id,'itemname':itemname,'unit':unit,'quantity':quantity,'minimumquantity':minimumquantity,'moq':moq,})

def get_stock_by_itemname(itemname):
    with conn:
        c.execute("SELECT * FROM stock WHERE itemname=:itemname",{'itemname':itemname})
        return c.fetchall()
    
def get_stock_by_id(id):
    with conn:
        c.execute("SELECT * FROM stock WHERE id=:id",{'id':id})
        return c.fetchall()
    
def get_stock_by_unit(unit):
    with conn:
        c.execute("SELECT * FROM stock WHERE unit=:unit",{'unit':unit})
        return c.fetchall()

def delete_stock_itemname(itemname):
    with conn:
        c.execute("DELETE FROM stock WHERE itemname=:itemname",{'itemname':itemname})

def delete_stock_id(id):
    with conn:
        c.execute("DELETE FROM stock WHERE id=:id",{'id':id})

def update_stock(itemname,quantity):
    with conn:
        c.execute("UPDATE stock SET quantity = :quantity WHERE itemname = :itemname",{'quantity':quantity,'itemname':itemname})

def getallstock():
    with conn:
        c.execute("SELECT * FROM stock")
        return c.fetchall()

def getallitem_names():
    with conn:
        c.execute("SELECT itemname FROM stock")
        return c.fetchall()
