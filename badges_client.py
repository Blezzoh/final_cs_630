import badges_pb2
import badges_pb2_grpc
import time
import grpc 

# serializer and deserializer
from google.protobuf.json_format import MessageToJson, ParseDict
import json

def run(conn_in,conn_out, table, type):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = badges_pb2_grpc.BadgeServiceStub(channel)
        #origin
        f_in = open(conn_in)
        origin_json = json.load(f_in)
        origin = ParseDict(origin_json, badges_pb2.ConnectionIO())
        #destination 
        f_out= open(conn_out)
        dest_json = json.load(f_out)
        destination = ParseDict(dest_json, badges_pb2.ConnectionIO())
        stub_request = badges_pb2.MigrationRequest(origin = origin, destination = destination, table=table, type=type)
        stub_reply = stub.MigrateData(stub_request)
        # for i in stub_reply:
        print(stub_reply.outcome)
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
                        help='mysql or nosql')
    args = parser.parse_args()
    run(conn_in=args.conn_in, conn_out=args.conn_out, table = args.table, type= args.type)          
