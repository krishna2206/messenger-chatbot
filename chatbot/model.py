from datetime import datetime

from pymongo import MongoClient
from tinydb import TinyDB, Query
import tinydb_encrypted_jsonstorage as tes


class Model:
    def __init__(self, config):
        """
        If the database type is MongoDB, then connect to the database using the connection string or host and port, and then
        get the database name
        """
        self.DB_TYPE = config.DB_TYPE
        if self.DB_TYPE == "MONGODB":
            self.db = (
                MongoClient(config.DB_CONNECTION_STRING)
                if config.DB_CONNECTION_STRING != ""
                else MongoClient(config.DB_HOST, config.DB_PORT))
            self.db = self.db[config.DB_NAME]
        elif self.DB_TYPE == "TINYDB":
            """
            self.db = TinyDB(
                encryption_key=config.DB_ENCRYPTION_KEY,
                path=config.DB_FILE,
                storage=tes.EncryptedJSONStorage)
            """
            self.db = TinyDB(
                path=config.DB_FILE)

        self.__init_db()

    def __init_db(self):
        """
        If the database is empty, insert a dummy document
        """
        if self.DB_TYPE == "MONGODB":
            if len(self.db.list_collection_names()) == 0:
                users = self.db.users
                users.insert_one({
                    "user_id": "0000000000000000",
                    "query": None,
                    "last_use": datetime.now().timestamp()
                })
        elif self.DB_TYPE == "TINYDB":
            if len(self.db.tables()) == 0:
                users = self.db.table("users")
                users.insert({
                    "user_id": "0000000000000000",
                    "query": None,
                    "last_use": datetime.now().timestamp()
                })

    def update_user(self, user_id, **new_assignments):
        if self.DB_TYPE == "MONGODB":
            users = self.db.users

            user_query = {"user_id": user_id}
            new_value = {
                "$set": {"last_use": datetime.now().timestamp()}
            }
            new_value.update(new_assignments)

            users.update_one(user_query, new_value)
        elif self.DB_TYPE == "TINYDB":
            new_assignment = {
                "last_use": datetime.now().timestamp()
            }

            self.db.update(new_assignment, Query().user_id.exists())

    def get_user(self, user_id):
        if self.DB_TYPE == "MONGODB":
            users = self.db.users
            user_query = {"user_id": user_id}

            return users.find_one(user_query)
        elif self.DB_TYPE == "TINYDB":
            return self.db.get(Query().user_id == user_id)

    def add_user(self, user_id):
        if self.DB_TYPE == "MONGODB":
            users = self.db.users
            users.insert_one({
                "user_id": user_id,
                "query": None,
                "last_use": datetime.now().timestamp()
            })
        elif self.DB_TYPE == "TINYDB":
            users = self.db.table("users")
            users.insert({
                "user_id": user_id,
                "query": None,
                "last_use": datetime.now().timestamp()
            })

    def get_query(self, user_id):
        if self.DB_TYPE == "MONGODB":
            users = self.db.users
            user_query = {"user_id": user_id}

            return users.find_one(user_query).get("query")
        elif self.DB_TYPE == "TINYDB":
            user_query = Query()
            print(self.db.get(user_query.user_id == user_id))
            return self.db.get(Query().user_id == user_id).get("query")

    def add_query(self, user_id, action, **action_params):
        if self.DB_TYPE == "MONGODB":
            users = self.db.users

            user_query = {"user_id": user_id}
            new_value = {
                "$set": {"query": {"action": action}}
            }
            if action_params != {}:
                new_value["$set"]["query"]["params"] = action_params

            users.update_one(user_query, new_value)
        elif self.DB_TYPE == "TINYDB":
            new_assignment = {
                "query": {"action": action}
            }
            if action_params != {}:
                new_assignment["query"]["params"] = action_params

            self.db.update(new_assignment, Query().user_id.exists())

    def remove_query(self, user_id):
        if self.DB_TYPE == "MONGODB":
            users = self.db.users

            user_query = {"user_id": user_id}
            new_value = {
                "$set": {"query": None}
            }

            users.update_one(user_query, new_value)
        elif self.DB_TYPE == "TINYDB":
            new_assignment = {"query": None}

            self.db.update(new_assignment, Query().user_id.exists())
