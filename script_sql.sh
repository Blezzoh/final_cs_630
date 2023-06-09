py badges_client.py --conn_in=./data/connection_local_badges.json --conn_out=./data/connection_azure.json --table=orders --type=mysql
py badges_client.py --conn_in=./data/connection_local_badges.json --conn_out=./data/connection_azure.json --table=postlinks --type=mysql

py badges_client.py --conn_in=./data/connection_local_badges.json --conn_out=./data/connection_local_mongo.json --table=orders --type=mysql_to_mongo
py badges_client.py --conn_in=./data/connection_local_badges.json --conn_out=./data/connection_azure_mongo.json --table=orders --type=mysql_to_mongo

py badges_client.py --conn_in=./data/connection_azure_mongo.json --conn_out=./data/connection_local_mongo.json --table=orders --type=mongo

py badges_client.py --conn_in=./data/connection_azure_mongo.json --conn_out=./data/connection_local_badges.json --table=orders --type=mongo_to_mysql
py badges_client.py --conn_in=./data/connection_local_mongo.json --conn_out=./data/connection_local_badges.json --table=orders --type=mongo_to_mysql
py badges_client.py --conn_in=./data/connection_local_mongo.json --conn_out=./data/connection_aws_sql.json --table=orders --type=mongo_to_mysql