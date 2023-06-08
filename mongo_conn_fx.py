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

def drop_collection_if_exist(db, collection):
    lst = db.list_collection_names()
    if collection in lst:
        db[collection].drop()
    return db[collection]

def get_cursor_for_all_documents(db):
    return db.find({})

def get_all_documents_in_mongo_db(db):
    return list(db.find({}))


def get_documents_from_mongodb(client, db_name, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    return list(collection.find())
    
    
def get_documents_from_mongodb_w_converted_id(client, db_name, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    lst =  list(collection.find())
    if lst[0]["_id"] != None:
        values = []
        for item in lst:
            item["_id"] = item["_id"].toString()
            values.append(item)
        return values
    return lst