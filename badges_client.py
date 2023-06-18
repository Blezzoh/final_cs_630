import badges_pb2
import badges_pb2_grpc
import time
import grpc

import time

# serializer and deserializer
from google.protobuf.json_format import MessageToJson, ParseDict
import json

def gen_sql_connection_object(conn_path):
    f = open(conn_path)
    conn_json = json.load(f)
    return ParseDict(conn_json, badges_pb2.ConnectionIOSQL())

def gen_mongo_connection_object(conn_path):
    f = open(conn_path)
    conn_json = json.load(f)
    return ParseDict(conn_json, badges_pb2.ConnectionIOMongo())

def run(conn_in,conn_out, table, type):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = badges_pb2_grpc.BadgeServiceStub(channel)
        if(type == "mysql"):
            #origin
            origin = gen_sql_connection_object(conn_in)
            #destination 
            destination = gen_sql_connection_object(conn_out)
            st = time.time()
            stub_request = badges_pb2.MigrationRequestSQL(origin = origin, destination = destination, table=table, type=type)
            stub_reply = stub.MigrateDataSQL(stub_request)
            # for i in stub_reply:
            ed = time.time()
            tm = "overall: seconds {} milliseconds {}".format((ed -st), (ed -st) * 1000)
            print(stub_reply.outcome)
            print(tm)
        
        if type == "mysql_to_mongo":
            origin = gen_sql_connection_object(conn_in)
            destination = gen_mongo_connection_object(conn_out)
            
            st = time.time()
            
            stub_request = badges_pb2.MigrationRequestSQLToMongo(origin = origin, destination = destination, table=table, type=type)
            stub_reply = stub.MigrateDataSQLToMongo(stub_request)
            
            ed = time.time()
            tm = "overall: seconds {} milliseconds {}".format((ed -st), (ed -st) * 1000)
            
            print(stub_reply.outcome)
            print(tm)
        
        if type == "mongo":
            origin = gen_mongo_connection_object(conn_in)
            destination = gen_mongo_connection_object(conn_out)
            
            st = time.time()
            
            stub_request = badges_pb2.MigrationRequestMongo(origin = origin, destination = destination, table=table, type=type)
            stub_reply = stub.MigrateDataMongo(stub_request)
            
            ed = time.time()
            tm = "overall: seconds {} milliseconds {}".format((ed -st), (ed -st) * 1000)
            
            print(stub_reply.outcome)
            print(tm)
        
        if type == "mongo_to_mysql":
            origin = gen_mongo_connection_object(conn_in)
            destination = gen_sql_connection_object(conn_out)
            
            st = time.time()
            
            stub_request = badges_pb2.MigrationRequestMongoToSQL(origin = origin, destination = destination, table=table, type=type)
            stub_reply = stub.MigrateDataMongoToSQL(stub_request)
            
            ed = time.time()
            tm = "overall: seconds {} milliseconds {}".format((ed -st), (ed -st) * 1000)
            
            print(stub_reply.outcome)
            print(tm)
        
        

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='provide path to connection object')
    parser.add_argument('--conn_in', metavar='conn_in', required=True,
                        help='path to the origin connection object')
    parser.add_argument('--conn_out', metavar='conn_out', required=True,
                        help='path to the destination connection object')
    parser.add_argument('--table', metavar='table', required=True,
                        help='name of table to migrate')
    parser.add_argument('--type', metavar='type', required=True,
                        help='mysql or mon')
    args = parser.parse_args()
    run(conn_in=args.conn_in, conn_out=args.conn_out, table = args.table, type= args.type)          
