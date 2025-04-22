import sqlite3

conn = sqlite3.connect('ims.db') #:memory:
c = conn.cursor()

'''c.execute ("""CREATE TABLE bills (
          erno text,
          itemname text,
          suppliername text,
          quantity int,
          rate int,
          amount int,
          dateday int,
          datemonth int,
          dateyear int,
          projectname text
          )""")
conn.commit()'''

class bill():
    def __init__(self,erno,itemname,suppliername,quantity,rate,amount,dateday,datemonth,dateyear,projectname):
        self.erno = erno
        self.itemname = itemname
        self.suppliername=suppliername
        self.quantity=quantity
        self.rate=rate
        self.amount=amount
        self.dateday=dateday
        self.datemonth=datemonth
        self.dateyear=dateyear
        self.projectname=projectname

sbill= bill('12345','Aarav','Mehta','12','1','2','9','2','2024','b2')


def new_bill(erno,itemname,suppliername,quantity,rate,amount,dateday,datemonth,dateyear,projectname):
    with conn:
        c.execute("INSERT INTO bills VALUES (:erno,:itemname,:suppliername,:quantity,:rate,:amount,:dateday,:datemonth,:dateyear,:projectname)",
        {'erno':erno,'itemname':itemname,'suppliername':suppliername,'quantity':quantity,'rate':rate,'amount':amount,'dateday':dateday,'datemonth':datemonth,'dateyear':dateyear,'projectname':projectname})

def get_by_itemname(itemname):
    with conn:
        c.execute("SELECT * FROM bills WHERE itemname=:itemname",{'itemname':itemname})
        return c.fetchall()
    
def get_by_erno(erno):
    with conn:
        c.execute("SELECT * FROM bills WHERE erno=:erno",{'erno':erno})
        return c.fetchall()
    
def get_by_suppliername(suppliername):
    with conn:
        c.execute("SELECT * FROM bills WHERE suppliername=:suppliername",{'suppliername':suppliername})
        return c.fetchall()
    
def get_by_date(dateday,datemonth,dateyear):
    with conn:
        c.execute("SELECT * FROM bills WHERE dateday=:dateday and datemonth=:datemonth and dateyear=:dateyear",{'dateday':dateday , 'datemonth':datemonth, 'dateyear':dateyear})
        return c.fetchall()
    
def get_by_month(datemonth,dateyear):
    with conn:
        c.execute("SELECT * FROM bills WHERE datemonth=:datemonth and dateyear=:dateyear",{'datemonth':datemonth, 'dateyear':dateyear})
        return c.fetchall()
    
def get_by_year(dateyear):
    with conn:
        c.execute("SELECT * FROM bills WHERE dateyear=:dateyear",{'dateyear':dateyear})
        return c.fetchall()
   
def get_by_projectname(projectname):
    with conn:
        c.execute("SELECT * FROM bills WHERE projectname=:projectname",{'projectname':projectname})
        return c.fetchall()
    
def delete(itemname):
    with conn:
        c.execute("DELETE FROM bills WHERE itemname=:itemname",{'itemname':itemname})

def getallbills():
    with conn:
        c.execute("SELECT * FROM bills")
        return c.fetchall()
