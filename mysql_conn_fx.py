import mysql.connector
from mysql.connector import FieldType
import datetime

def connect_to_sql_with_login_no_port(usernm, pwd, hst, dba):
    try:
        conn = mysql.connector.connect(user=usernm, password = pwd, host=hst, database = dba)
        return conn
    except mysql.connector.Error as err: 
        print(err)
        return None


def connect_to_sql_with_login(usernm, pwd, hst, dba, prt):
    try:
        conn = mysql.connector.connect(user=usernm, password = pwd, host=hst, database = dba, port=prt)
        return conn
    except mysql.connector.Error as err: 
        print(err)
        return None
    
def connect_to_sql_with_json(config):
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err: 
        print(err)
        return None


def get_cursor_and_rows_read_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM "+ table_name +";")
    rows = cursor.fetchall()
    return [cursor, rows]



def create_map_from_cursor(cursor, rows):
    lst =[]
    for item in rows:
        mp = get_column_from_cursor(cursor.description,item)
        lst.append(mp)
    return lst

def get_table_columns_statement(description):
    mp = {}
    for i in range(len(description)):
        descr = description[i]
        isNull = "NULL" if descr[6] == 1 else "NOT NULL"
        name = descr[0]
        kind = FieldType.get_info(descr[1]) if FieldType.get_info(descr[1]) != "VAR_STRING" else "VARCHAR(250)"
        mp[name] = kind + " " + isNull
    return mp

def get_column_from_cursor(description, row):
    mp = {}
    for i in range(len(description)):
        descr = description[i]
        mp[descr[0]] = row[i]
        if isinstance(row[i], datetime.date):
           mp[descr[0]] = row[i].strftime("%Y-%m-%d") 
        if isinstance(row[i], datetime.datetime):
           mp[descr[0]] = row[i].strftime("%Y-%m-%d %H:%M:%S") 
    return mp

def close_connection(connection):
    connection.close()


