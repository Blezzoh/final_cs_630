import pymongo

field_type = {
 0: 'DECIMAL',
 1: 'TINY',
 2: 'SHORT',
 3: 'LONG',
 4: 'FLOAT',
 5: 'DOUBLE',
 6: 'NULL',
 7: 'TIMESTAMP',
 8: 'LONGLONG',
 9: 'INT24',
 10: 'DATE',
 11: 'TIME',
 12: 'DATETIME',
 13: 'YEAR',
 14: 'NEWDATE',
 15: 'VARCHAR',
 16: 'BIT',
 246: 'NEWDECIMAL',
 247: 'INTERVAL',
 248: 'SET',
 249: 'TINY_BLOB',
 250: 'MEDIUM_BLOB',
 251: 'LONG_BLOB',
 252: 'BLOB',
 253: 'VAR_STRING',
 254: 'STRING',
 255: 'GEOMETRY' 
 }

def get_sql_schema_from_mongo_document(doc):
    keysList = list(doc.keys())
    dic_types = {}
    for key in keysList:
        k = doc[key]
        if isinstance(k, int):
            dic_types[key] = "LONG NULL"
        # TODO: add more types
        if isinstance(k, float):
            dic_types[key] = "DOUBLE NULL"
        if isinstance(k, str):
            dic_types[key] = "TEXT NULL"
        if key == "_id":
            dic_types["_id"] = "VARCHAR(50) NOT NULL"
        if k is None:
            dic_types[key] = "TEXT NULL"
    return dic_types
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
    return list(collection.find({}))
    
    
def get_documents_from_mongodb_w_converted_id(client, db_name, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    # print( collection.find())
    lst =  list(collection.find())
    if lst[0]["_id"] != None:
        values = []
        for item in lst:
            item["_id"] = str(item["_id"])
            values.append(item)
        return values
    return lst