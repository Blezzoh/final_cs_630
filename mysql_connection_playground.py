import mysql.connector
from mysql.connector import FieldType
# from mysql.connector import FieldFlag

# nanoorm\nanoorm.py
import json
from nanosql.nanoorm import create_table
from data.credentials_msql_local import username, pw, host, db, port, table_badge
from mysql_conn_fx import close_connection, connect_to_sql_with_json, get_cursor_and_rows_read_table, create_map_from_cursor,get_column_from_cursor,get_table_columns_statement

config = {
  'host':'instance630sql.mysql.database.azure.com',
  'user':'blaira',
  'password':'cs_630_server',
  'database':'cs_630',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': './data/DigiCertGlobalRootG2.crt.pem',
  "table": "badges"
}
# username = "root"
# pw = "160496"
# host = "localhost"
# db = "cs_630"
# table_badge = "badges"
# port = "3306"
# jdbc_conn_str = "jdbc:mysql://localhost:3306/?user=root"
# odbc_conn_str = "root@localhost:3306"
config2 ={
    "host": host,
    "user": username,
    "password": pw,
    "port": port,
    "database": db,
    "table": "badges"
}
columns = {
   "col1": "LONG NOT NULL",
   "col2": "TEXT NULL"
}
conn = None
# conn = connect_to_sql_with_json(config2)

print(json.dumps(config))
if(conn != None):
    print("it worked")
    (cursor, rows) = get_cursor_and_rows_read_table(conn, table_badge)
    # print(create_map_from_cursor(cursor, rows))
    for i in range(1):
      descr = cursor.description[i]
    #   print("position: ", i)
      print("colname: ", descr[0])
      print("type: ", FieldType.get_info(descr[1]))
      print("null ok: ", descr[6])
      print(get_column_from_cursor(cursor.description, rows[0]))
    print(get_table_columns_statement(cursor.description))
      # print("flags: ", FieldFlag.desc)
      
    # print("description")
    # print(cursor.description)
    close_connection(conn)

# else:
#     print("it didn't")

print(create_table("my_table", **columns))