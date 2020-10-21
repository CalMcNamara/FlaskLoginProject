import sqlite3
from sqlite3 import Error

from passlib.context import CryptContext
import getpass

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)


def display_menu():
    status = input("Do you have an account? Y / N ")
    if(status == 'Y'):
        print('Y')
        login_user()
    elif(status == 'N'):
        print('N')
        create_user()
    else:
        print("Please Enter Y / N")
        display_menu()

def login_user():
    username = input("Please enter Username ")
    status = check_user_exists(username)
    if(status != True):
        print("Username does not exist. Please enter a correct one.")
        login_user()
    else:
        password = getpass.getpass("Please enter a password ")
        check_password(username,password)

def check_password(username, password):
    database = 'userlogin.db'
    conn = create_connection(database)
    cur = conn.cursor()

    sql = "SELECT password FROM userlogin WHERE username = " + "'" + username + "'"

    cur.execute(sql)
    rows = cur.fetchone()
    password_db = ''
    for row in rows:
        password_db = row
    if(check_encrypted_password(password,password_db) == True):
        print("Yes")
    else:
        print("password: " + str(password) + " passworddb: " + str(password_db))

def create_user():
    username = input("Please enter Username ")
    password = getpass.getpass("Please enter a password ")
    repassword = getpass.getpass("Please Re-enter password ")

    if(password == repassword):
        print('Password matches, moving on. ')
    else:
        print('Password do not match please retry ')
        create_user()
    status = check_user_exists(username)

    if(status != False): 
        print('Please Try again. Username ' + username + " is unavaliable.")
        create_user()
    else:
        print("Username is avaliable ")
        add_user(username, password)

def check_user_exists(username):
    # called from create_user() returns true or false if user is already in the db. 
    database = 'userlogin.db'
    conn = create_connection(database)
    cur = conn.cursor()

    sql = "SELECT * FROM userlogin WHERE username = " + "'" + username + "'"
    cur.execute(sql)
    rows = cur.fetchone()
    if(rows == None):
        status = False
    else:
        status = True

    return(status)
    
def add_user(username, password):
    # adds the user to the db. 
    database = 'userlogin.db'
    conn = create_connection(database)
    cur = conn.cursor()
    password = encrypt_password(password)
    sql = '''INSERT INTO userlogin (username,password)VALUES(?,?)'''
    data = (username,password)
    cur.execute(sql,data)
    conn.commit()

    return True 

def create_connection(db_file):
    """ create a database connection to a SQLite Database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def main():
    database = 'userlogin.db'
    conn = create_connection(database)
    display_menu()
if __name__ == '__main__':
    main()
