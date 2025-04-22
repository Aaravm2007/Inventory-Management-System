import sqlite3
import base64

conn = sqlite3.connect('ims.db') #:memory:
c = conn.cursor()

'''c.execute ("""CREATE TABLE users (
           username text PRIMARY KEY,
           password text,
           email text,
           phone text,
           role text
           )""")
conn.commit()'''

def new_user(username,ue_password,email,phone,role):
    password=encrypt_password(ue_password)
    with conn:
        c.execute("INSERT INTO users VALUES (:username,:password,:email,:phone,:role)",
        {'username':username,'password':password,'email':email,'phone':phone,'role':role,})

def get_user_by_username(username):
    with conn:
        c.execute("SELECT * FROM users WHERE username=:username",{'username':username})
        return c.fetchall()

def get_user_by_email(email):
    with conn:
        c.execute("SELECT * FROM users WHERE email=:email",{'email':email})
        return c.fetchall()

def get_user_by_phone(phone):
    with conn:
        c.execute("SELECT * FROM users WHERE phone=:phone",{'phone':phone})
        return c.fetchall()
    
def delete_user_username(username):
    with conn:
        c.execute("DELETE FROM users WHERE username=:username",{'username':username})

def update_user(username,password,email,phone,role):
    with conn:
        c.execute("UPDATE users SET password = :password,email = :email,phone = :phone,role = :role WHERE username = :username",
        {'password':password,'email':email,'phone':phone,'role':role,'username':username})

def getallusers():
    with conn:
        c.execute("SELECT * FROM users")
        return c.fetchall()

def getallusernames():
    with conn:
        c.execute("SELECT username FROM users")
        return c.fetchall()
    
def check_login(username,ue_password):
    with conn:
        c.execute("SELECT password FROM users WHERE username=:username",{'username':username})
        result = c.fetchone()
        if result:
            stored_password = decrypt_password(result[0])
            if stored_password == ue_password:
                return True
    return False
    
def encrypt_password(password):
    encrypted_password=base64.b64encode(password.encode("utf-8"))
    return encrypted_password

def decrypt_password(encrypted_password):
    decrypted_password=base64.b64decode(encrypted_password).decode("utf-8")
    return decrypted_password

def check_role(username):
    with conn:
        c.execute("SELECT role FROM users WHERE username=:username",{'username':username})
        return c.fetchall()