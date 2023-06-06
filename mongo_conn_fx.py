import pymongo

def get_mongo_client(conn_str):
    return pymongo.MongoClient(conn_str)

def close_mongo_connection(client):
    client.close()

# return a list of databases name
def get_client_databases(client):
    return client.list_database_names()

#creates a database or retrieve one if it exists
def create_mongo_db(client, db_name):
    return client[db_name]

def insert_one_mongodb(db, single_dict_item):
    db.insert_one(single_dict_item)

def insert_many_mongdb(db, list_dict_items):
    db.insert_many(list_dict_items)

def drop_mongo_db(client, db_name):
    client.drop_database(db_name)

def drop_and_create_mongo_db(client, db_name):
    db_lst= get_client_databases(client)
    if db_name in db_lst:
        client.drop_database(client, db_name)
    return client[db_name]

def get_cursor_for_all_documents(db):
    return db.find({})

def get_all_documents_in_mongo_db(db):
    return list(db.find({}))
    
