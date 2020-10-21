import sqlite3
from sqlite3 import Error






def create_connection(db_file):
    """ create a database connection to a SQLite Database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE STATEMENT
    :return: 
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_into_test(conn, data):
    sql = '''INSERT INTO userlogin (username,password)VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    return cur.lastrowid

def get_items(conn):
    sql = '''SELECT * FROM userlogin'''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)

def main():
    database = 'userlogin.db'
    sql_create_project_table = """ CREATE TABLE IF NOT EXISTS userlogin (
        username string PRIMARY KEY,
        password string NOT NULL)"""
    conn = create_connection(database)
    if conn is not None:
        create_table(conn,sql_create_project_table)
    else:
        print("Error! Cannot create the database connection.")
    with conn:
       # data = ('Example','Passcode')
       # insert_into_test(conn,data)
        get_items(conn)
if __name__ == '__main__':
    main()