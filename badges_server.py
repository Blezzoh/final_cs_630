from concurrent import futures
import time
import logging

import grpc
import badges_pb2
import badges_pb2_grpc
import json
from nanosql.nanoorm import create_table, drop_table_if_exist, insert

from mysql_conn_fx import close_connection, connect_to_sql_with_login, get_cursor_and_rows_read_table,get_column_from_cursor, connect_to_sql_with_json, get_table_columns_statement, create_map_from_cursor
from pymongo.errors import ConnectionFailure

from mongo_conn_fx import close_mongo_connection, create_mongo_db, get_mongo_client, drop_collection_if_exist,get_documents_from_mongodb
from mongo_conn_fx import get_documents_from_mongodb_w_converted_id,get_sql_schema_from_mongo_document
# serializer and deserializer
from google.protobuf.json_format import ParseDict, MessageToJson, MessageToDict


def create_and_move_data_to_mongo(client, db_name, collection_name, data):
    dest_db = create_mongo_db( client, db_name)
    dest_collection = drop_collection_if_exist(dest_db,collection_name)
    result = dest_collection.insert_many(data)
    return result.inserted_ids

class Badger(badges_pb2_grpc.BadgeServiceServicer):
    def MigrateDataMongoToSQL(self, request, context):
        conn_in_dict = MessageToDict(request.origin, preserving_proto_field_name=True)
        conn_out_dict = MessageToDict(request.destination, preserving_proto_field_name=True)
        table = request.table
        origin_db_name = conn_in_dict['database']
        conn_in = get_mongo_client(conn_in_dict['connectionString'])
        # print(conn_in_dict['connectionString'])
        try:
            conn_in.admin.command("ping")
            conn_out = connect_to_sql_with_json(conn_out_dict)
            if conn_out != None:
                #getting documents from mongo and making sql schema script
                #reading
                st_s = time.time()
                # print(conn_in_dict['connectionString'])
                
                list_data = get_documents_from_mongodb_w_converted_id(conn_in, origin_db_name, table)
                ed_s = time.time()
                # print(conn_in_dict['connectionString'])
                
                
                sql_schema_object = get_sql_schema_from_mongo_document(list_data[0])
                sql_create_stment = create_table(table, **sql_schema_object)
                
                # needs to get the schema for the table. Needs a function
                cursor_out = conn_out.cursor()
                drp_table_if_exists = drop_table_if_exist(table)
                cursor_out.execute(drp_table_if_exists)
                cursor_out.execute(sql_create_stment)
                # print(sql_create_stment)
                # conn_out.commit()
                
                st_d = time.time()
                for i in range(len(list_data)):
                    item = list_data[i]
                    insert_stmt = insert(table, **item)
                    # print(insert_stmt)
                    cursor_out.execute(insert_stmt)
        
                conn_out.commit()
                ed_d = time.time()
                
                cursor_out.close()
                r=(ed_s -st_s) * 1000 
                w=(ed_d -st_d) * 1000
                close_mongo_connection(conn_in)
                close_connection(conn_out)
                msg = "created {nrows} rows in {tbl}. read time: {r}. write time: {w}".format(nrows=len(list_data), tbl=table,r=r,w=w)
                # print(msg)
                return badges_pb2.MigrationReply(outcome=msg)
                
            else:
                print("connection to destination didn't work!")
                return badges_pb2.MigrationReply(outcome="connection to destination didn't work!") 
            
        except ConnectionFailure:
            print("connection to origin didn't work!")
            return badges_pb2.MigrationReply(outcome="connection to origin didn't work!") 
        
    def MigrateDataMongo(self, request, context):
        conn_in_dict = MessageToDict(request.origin, preserving_proto_field_name=True)
        conn_out_dict = MessageToDict(request.destination, preserving_proto_field_name=True)
        table = request.table
        origin_db_name = conn_in_dict['database']
        destination_db_name = conn_out_dict['database']
        
        conn_in = get_mongo_client(conn_in_dict['connectionString'])
        
        try:
            conn_in.admin.command("ping")
            conn_out = get_mongo_client(conn_out_dict['connectionString'])
            try:
                conn_out.admin.command("ping")
                
                st_s = time.time()
                list_data = get_documents_from_mongodb(conn_in, origin_db_name, table)
                
                ed_s = time.time()
                
                st_d = time.time()
                result_ids = create_and_move_data_to_mongo(conn_out, destination_db_name, table, list_data)
                
                
                ed_d = time.time()
                #cleaning
                close_mongo_connection(conn_out)
                close_mongo_connection(conn_in)
                nrows = len(result_ids)
                
                msg = "created {nrows} rows in {tbl}. read time: {r}. write time: {w}".format(nrows=nrows, tbl=table,r=(ed_s -st_s) * 1000 ,w=(ed_d -st_d) * 1000)
                print(msg)
                return badges_pb2.MigrationReply(outcome=msg)
            
            except ConnectionFailure:
                print("connection to destination didn't work!")
                return badges_pb2.MigrationReply(outcome="connection to destination didn't work!") 
        except ConnectionFailure:
            print("connection to origin didn't work!")
            return badges_pb2.MigrationReply(outcome="connection to origin didn't work!") 
        
    def MigrateDataSQLToMongo(self, request, context):
        conn_in_dict = MessageToDict(request.origin, preserving_proto_field_name=True)
        conn_out_dict = MessageToDict(request.destination, preserving_proto_field_name=True)
        table = request.table
        # print(conn_out_dict)
        destination_db_name = conn_out_dict['database']
        conn_in = connect_to_sql_with_json(conn_in_dict)
        if conn_in != None:
            client_out = get_mongo_client(conn_out_dict['connectionString'])
            try:
                client_out.admin.command("ping")
                # connection to mysql origin and getting a list of data
                (cursor_in, rows_in) = get_cursor_and_rows_read_table(conn_in, table)
                # print("connected with all the tables")
                st_s = time.time()
                list_data = create_map_from_cursor(cursor_in, rows_in)
                ed_s = time.time()
                
                # moving data to mongo db
                st_d = time.time()
                result_ids = create_and_move_data_to_mongo(client_out, destination_db_name, table, list_data)
                
                nrows = len(result_ids)
                
                #cleaning
                close_mongo_connection(client_out)
                ed_d = time.time()
                
                cursor_in.close()
                close_connection(conn_in)
                msg = "created {nrows} rows in {tbl}. read time: {r}. write time: {w}".format(nrows=nrows, tbl=table,r=(ed_s -st_s) * 1000 ,w=(ed_d -st_d) * 1000)
                # print(msg)
                return badges_pb2.MigrationReply(outcome=msg)
            
            except ConnectionFailure:
                print("connection to destination didn't work!")
                return badges_pb2.MigrationReply(outcome="connection to destination didn't work!") 
        else:
            print("connection to origin didn't work!")
            return badges_pb2.MigrationReply(outcome="connection to origin didn't work!")

    def MigrateDataSQL(self, request, context):
        conn_in_dict = MessageToDict(request.origin, preserving_proto_field_name=True)
        conn_out_dict = MessageToDict(request.destination, preserving_proto_field_name=True)
        table = request.table
        conn_in = connect_to_sql_with_json(conn_in_dict)
        if conn_in != None:
            conn_out = connect_to_sql_with_json(conn_out_dict)
            
            if(conn_out != None):
                st_s = time.time()
                (cursor_in, rows_in) = get_cursor_and_rows_read_table(conn_in, table)
                ed_s = time.time()
                # print("connected with all the tables")
                cursor_out = conn_out.cursor()
                drp_table_if_exists = drop_table_if_exist(table)
                table_columns = get_table_columns_statement(cursor_in.description)
                create_table_stmt = create_table(table, **table_columns)
                # print(create_table_stmt)
                cursor_out.execute(drp_table_if_exists)
                cursor_out.execute(create_table_stmt)
                conn_out.commit()
                # print(drp_table_if_exists)
                # print(create_table_stmt)

                # print(drp_table_if_exists+"\n" + create_table_stmt +"\n")
                st_d = time.time()
                for i in range(len(rows_in)):
                    item = rows_in[i]
                    data_map = get_column_from_cursor(cursor_in.description, item)
                    insert_stmt = insert(table, **data_map)
                    cursor_out.execute(insert_stmt)
                    # print(i)
                    # print(" ")
                    # yield badges_pb2.MigrationReply(outcome=format("executed %s", insert_stmt))
                conn_out.commit()
                ed_d = time.time()
                cursor_out.close()
                msg = "created {nrows} rows in {tbl}. read time: {r}. write time: {w}".format(nrows=len(rows_in), tbl=table,r=(ed_s -st_s) * 1000 ,w=(ed_d -st_d) * 1000)
            
                # print(msg)
                close_connection(conn_out)
                cursor_in.close()
                close_connection(conn_in)
                return badges_pb2.MigrationReply(outcome=msg)
            else:
                print("connection to destination didn't work!")
                close_connection(conn_in)
                return badges_pb2.MigrationReply(outcome="connection to destination didn't work!")
        else:
            print("connection to origin didn't work!")
            return badges_pb2.MigrationReply(outcome="connection to origin didn't work!")
   
    def GetBadgesMysql(self, request,context):
        conn = connect_to_sql_with_login(request.username, request.password, request.host, request.database, request.port)
        if conn != None:
            (cursor, rows) = get_cursor_and_rows_read_table(conn, request.table)
            rpc_data = badges_pb2.Badges()
            for i in range(len(rows)):
                if i == 0:
                    print(rows[i])
                current = rows[i]
                a_badge = badges_pb2.Badge(Id = current[0], UserId = current[1], Name= current[2], Date = current[3], 
                                           Class = current[4], TagBased = current[5])
                rpc_data.badges.append(a_badge)
            close_connection(conn)
            return rpc_data
        else:
            print("none.")
            return None
        
    def GetStreamBadgeMysql(self, request, context):
        conn = connect_to_sql_with_login(request.username, request.password, request.host, request.database, request.port)
        if conn != None:
            (cursor, rows) = get_cursor_and_rows_read_table(conn, request.table)
            for i in range(len(rows)):
                current = rows[i]
                a_badge = badges_pb2.Badge(Id = current[0], UserId = current[1], Name= current[2], Date = current[3], 
                                           Class = current[4], TagBased = current[5])
                yield a_badge
            close_connection(conn)
        else:
            return None
    def GetStreamBadge(self, request,context):

        f = open("data/badges.json")
        #returns json object as a dictionary
        data = json.load(f)

        #to protobuf
        for item in data:
            a_badge = ParseDict(item, badges_pb2.Badge())
            yield a_badge
    

    def GetBadges(self, request, context):
         #open temp data
        f = open("data/badges.json")
        #returns json object as a dictionary
        data = json.load(f)
        #to protobuf
        rpc_data = badges_pb2.Badges()
        for item in data:
            a_badge = ParseDict(item, badges_pb2.Badge())
            rpc_data.badges.append(a_badge)

        return rpc_data


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    badges_pb2_grpc.add_BadgeServiceServicer_to_server(Badger(),server)
    server.add_insecure_port("localhost:" + port)
    server.start()
    print("Server start, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()