import pymongo

class Database:
    #no init method because no need to make multiple instances
    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    #tell python we're not using self
    @staticmethod
    def initialize():
        print('database initalizing')
        #only way to access it is through database object
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['navigator']

    @staticmethod
    def insert(collection, data):
        return Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        return Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)
