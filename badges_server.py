from concurrent import futures
import time
import logging

import grpc
import badges_pb2
import badges_pb2_grpc
import json
from nanosql.nanoorm import create_table, drop_table_if_exist, insert

from mysql_conn_fx import close_connection, connect_to_sql_with_login, get_cursor_and_rows_read_table,get_column_from_cursor, connect_to_sql_with_json, get_table_columns_statement

# serializer and deserializer
from google.protobuf.json_format import ParseDict, MessageToJson, MessageToDict


class Badger(badges_pb2_grpc.BadgeServiceServicer):
    def MigrateData(self, request, context):
        conn_in_dict = MessageToDict(request.origin, preserving_proto_field_name=True)
        conn_out_dict = MessageToDict(request.destination, preserving_proto_field_name=True)
        table = request.table
        conn_in = connect_to_sql_with_json(conn_in_dict)
        if conn_in != None:
            conn_out = connect_to_sql_with_json(conn_out_dict)
            
            if(conn_out != None):
                (cursor_in, rows_in) = get_cursor_and_rows_read_table(conn_in, table)
                print("connected with all the tables")
                cursor_out = conn_out.cursor()
                drp_table_if_exists = drop_table_if_exist(table)
                table_columns = get_table_columns_statement(cursor_in.description)
                print(drp_table_if_exists)
                create_table_stmt = create_table(table, **table_columns)
                print(create_table_stmt)
                cursor_out.execute(drp_table_if_exists)
                cursor_out.execute(create_table_stmt)
                print(create_table_stmt)

                print(drp_table_if_exists+"\n" + create_table_stmt +"\n")
                for i in range(len(rows_in)):
                    item = rows_in[i]
                    data_map = get_column_from_cursor(cursor_in.description, item)
                    if( i== 0):
                        print(type(data_map["orderDate"]))
                    insert_stmt = insert(table, **data_map)
                    cursor_out.execute(insert_stmt)
                    # print(i)
                    # print(" ")
                    # yield badges_pb2.MigrationReply(outcome=format("executed %s", insert_stmt))
                conn_out.commit()
                cursor_out.close()
                msg = "created {nrows} rows in {tbl}".format(nrows=len(rows_in), tbl=table)
                print(msg)
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
        print(conn_in_dict)
        print(conn_out_dict)
        rpc_data = MessageToJson(request.origin) + "\n\n" + MessageToJson(request.destination)
        rpc_resp = badges_pb2.MigrationReply()
        rpc_resp.outcome = rpc_data
        return rpc_resp
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