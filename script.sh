#generating corresponding python code
py -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. protos/badges.proto

# 3 ./data/connection_local_badges.json
# 4 ./data/connection_local_badges.json