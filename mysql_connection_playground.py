import mysql.connector
from mysql.connector import FieldType
# from mysql.connector import FieldFlag

# nanoorm\nanoorm.py
import json
from nanosql.nanoorm import create_table
from data.credentials_msql_local import username, pw, host, db, port, table_badge
from mysql_conn_fx import close_connection, connect_to_sql_with_json, get_cursor_and_rows_read_table, create_map_from_cursor,get_column_from_cursor,get_table_columns_statement
from mongo_conn_fx import get_mongo_client, get_documents_from_mongodb, close_mongo_connection, get_sql_schema_from_mongo_document

config2 ={
    "host": host,
    "user": username,
    "password": pw,
    "port": port,
    "database": db,
    "table": "badges"
}

config3 = {
    "connectionString":"mongodb://localhost:27017",
    "database": "cs_630"
}
columns = {
   "col1": "LONG NOT NULL",
   "col2": "TEXT NULL"
}




# conn = connect_to_sql_with_json(conn_s)

# if conn != None:
    # close_connection(conn)

# def test_mongo():
#   client = get_mongo_client(config3["connectionString"])
#   print(client.list_database_names())
#   print(client[config3["database"]].list_collection_names())
#   docs = get_documents_from_mongodb(client, config3["database"], "orders")
#   print(len(docs))
#   # print(get_sql_schema_from_mongo_document(docs[0]))
#   t = get_sql_schema_from_mongo_document(docs[0])
#   print(create_table("test", **t))
#   print(docs[0])
#   close_mongo_connection(client)


# test_mongo()


# conn = connect_to_sql_with_json(config2)

# print(json.dumps(config))
# if(conn != None):
#     print("it worked")
#     (cursor, rows) = get_cursor_and_rows_read_table(conn, table_badge)
#     # print(create_map_from_cursor(cursor, rows))
#     for i in range(1):
#       descr = cursor.description[i]
#     #   print("position: ", i)
#       print("colname: ", descr[0])
#       print("type: ", FieldType.get_info(descr[1]))
#       print("null ok: ", descr[6])
#       print(get_column_from_cursor(cursor.description, rows[0]))
#     print(get_table_columns_statement(cursor.description))
#       # print("flags: ", FieldFlag.desc)
      
#     # print("description")
#     # print(cursor.description)
#     close_connection(conn)

# else:
#     print("it didn't")

# print(create_table("my_table", **columns))







# recycle original client
# print(stub_reply)
        # if args[0] == "1":
        #     stub_reply = stub.GetBadges(badges_pb2.BadgeRequest(name = "all"))
        #     stub_to_str = MessageToJson(stub_reply)
        #     print(stub_to_str)
        # elif args[0] == "2": 
        #     stub_request = badges_pb2.BadgeRequest(name = "stream")
        #     stub_reply = stub.GetStreamBadge(stub_request)
        #     for badge in stub_reply:
        #         print("incoming ....\n\n")
        #         print(MessageToJson(badge))
        # #TODO: read file in argumes
        # #TODO: change the way we are receiving arguments
        # elif args[0] == "3":
        #     #TODO: remember to use the Connection string'
        #     f = open(args[1])
        #     data = json.load(f)
        #     print(data)
        #     stub_request = ParseDict(data, badges_pb2.Connection())
        #     stub_reply = stub.GetBadgesMysql(stub_request)
        #     print("len", len(stub_reply.badges))
        # elif args[0] == "4":
        #     #TODO: remember to use the Connection string'
        #     f = open(args[1])
        #     data = json.load(f)
        #     print(data)
        #     stub_request = ParseDict(data, badges_pb2.Connection())
        #     stub_reply = stub.GetStreamBadgeMysql(stub_request)
        #     for badge in stub_reply:
        #         print("incoming ....\n\n")
        #         print(MessageToJson(badge))