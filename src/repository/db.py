from pymongo import MongoClient


class MongoDatabaseConnection:
    __instance = None

    def __init__(self, db_name: str, mongo_hostname, mongo_username, mongo_password):
        if MongoDatabaseConnection.__instance is not None:
            raise Exception("Singleton instance already exists!")
        else:
            self.client = None
            self.mongo_hostname = mongo_hostname
            self.mongo_username = mongo_username
            self.mongo_password = mongo_password
            self.db = self.get_database(db_name=db_name)
            MongoDatabaseConnection.__instance = self

    @staticmethod
    def get_instance(db_name: str, mongo_hostname, mongo_username, mongo_password):
        if MongoDatabaseConnection.__instance is None:
            MongoDatabaseConnection(db_name, mongo_hostname, mongo_username, mongo_password)
        return MongoDatabaseConnection.__instance

    def get_database(self, db_name: str):
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        mongo_connection_string = f"mongodb+srv://{self.mongo_username}:{self.mongo_password}@{self.mongo_hostname}"
        self.client = MongoClient(mongo_connection_string)
        # Create the database for our example (we will use the same database throughout the tutorial)
        return self.client[db_name]

    def close_connection(self):
        self.client.close()

    def get_collection(self, collection_name: str):
        return self.db[collection_name]
