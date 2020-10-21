import sqlite3
from sqlite3 import Error

from passlib.context import CryptContext
import getpass

class UserLogin:

    def __init__(self, username, password):
        self.username = username
        self.password = str(password)
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000)
        self.hashed = ' '
        self.password_status = False
    
    
    # encrypts the password.
    def encrypt_password(self, password):
        self.hashed = self.pwd_context.encrypt(self.password)
    
    
    # checks if the encrypted password is correct.
    def check_encrypted_password(self, password, hashed):
        self.password_status = self.pwd_context.verify(password, hashed)


    def create_connection(self,db_file):
        """ create a database connection to a SQLite Database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn


    def check_password(self,username, password):
        database = 'userlogin.db'
        conn = self.create_connection(database)
        cur = conn.cursor()
        user_status = self.check_user_exists(username)
        if(user_status == False):
            # this means that there is no user under that username. 
            # returns False that the password does not exist. 
            return(False)
        else:
            sql = "SELECT password FROM userlogin WHERE username = " + "'" + username + "'"

            cur.execute(sql)
            rows = cur.fetchone()
            password_db = ''
        
            if(rows is None):
                print("None")
            else:
                for row in rows:
                    password_db = row
                if(self.check_encrypted_password(password,password_db) == True):
                    return(True)
                else:
                    return(False)
        

    def check_user_exists(self,username):
        # returns true or false if user is already in the db. 
        database = 'userlogin.db'
        conn = self.create_connection(database)
        cur = conn.cursor()
        sql = "SELECT * FROM userlogin WHERE username = " + "'" + username + "'"
        cur.execute(sql)
        rows = cur.fetchone()
        # if no usersname pulled from the db then return False that the user exists. 
        if(rows == None):
            status = False
            # else return True that there is a username already taken. 
        else:
            status = True
        return(status)

    def add_user(self):
        # adds the user to the db. 
        # ensure that there is no user with that username. 
        user_status = self.check_user_exists(self.username)
        
        #if there is a user with the same username return a false status. 
        if(user_status == True):
            return(False)
        
        else:
            self.password = self.encrypt_password(self.password)
            database = 'userlogin.db'
            conn = self.create_connection(database)
            cur = conn.cursor()
            password = self.hashed
            sql = '''INSERT INTO userlogin (username,password)VALUES(?,?)'''
            data = (self.username,self.hashed)
            
            cur.execute(sql,data)
            conn.commit()



        

def main():
    user = UserLogin('Billy','123123')
    encrytpass = user.encrypt_password(user.password)
    user.check_encrypted_password('1223',user.hashed)
    user.check_password('Herald','123123')
    user.add_user()
if __name__ == '__main__':
    main()