from abc import abstractmethod
from pymongo import MongoClient
from redis import Redis
from pymongo.errors import ServerSelectionTimeoutError, \
    AutoReconnect, ConnectionFailure, ConfigurationError, OperationFailure
from redis.exceptions import ConnectionError, TimeoutError, RedisError

class AbstractDbConnector:
    def __init__(
            self, 
            db_name:str, 
            db_host:str, 
            username:str,
            password:str, 
            port:int):

        self.db_name = db_name
        self.db_host = db_host
        self.username = username
        self.password = password
        self.port = port

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def insert(self, params):
        pass

    @abstractmethod
    def delete(self, params):
        pass

    @abstractmethod
    def update(self, params):
        pass


class MongoDbConnection(AbstractDbConnector):

    __number_of_connections = 0
    __connections = {}

    def __init__(
            self, 
            db_name:str, 
            db_host:str, 
            username:str,
            password:str, 
            port:int):
        """ Constructor.
        """
        super().__init__(db_name, db_host, username, password, port)

        for num_connection, config in MongoDbConnection.__connections.items():
            if config["db_name"] == db_name and config["db_host"] == db_host \
                and config["username"] == username and config["password"] == password \
                and config["port"] == port:
                
                raise Exception("You can't create another MongoDbConnection class")
        MongoDbConnection.__number_of_connections +=1
        MongoDbConnection.__connections[MongoDbConnection.__number_of_connections] \
            = {
                "db_name" : db_name,
                "db_host" : db_host,
                "username" : username,
                "password" : password,
                "port" : port
            }

    def connect(self):
        self.client = MongoClient(
                    host=self.db_host, 
                    port=self.port, 
                    username=self.username,
                    password=self.password)
        response = self.__check_connection_to_db()  
        return response


    def __check_connection_to_db(self):
        try:
            aux = self.client[self.db_name].command("ping")
            return "Connection Establish" 
        except ServerSelectionTimeoutError as err:
            raise(err)

    
    def insert(self, collection, params):
        try:
            if self.client[self.db_name][collection].count_documents(params, limit = 1):
                return("This document already has this data") 
            else:
                result = self.client[self.db_name][collection].insert_one(params)
                return result.acknowledged
        except OperationFailure as err:
            raise err
        finally:
            self.client.close()


    def get(self, collection, criteria):
        try:
            result = []
            for collect in self.client[self.db_name][collection].find(criteria):
                # collect.pop("_id")
                result.append(collect)
            if not result:
                message = "Nothing was found"
                return message
            else:
                return result
        except OperationFailure as err:
            raise err
        finally:
            self.client.close()


    def delete(self, collection, criteria):
        try:
            result = self.client[self.db_name][collection].delete_many(criteria) 
            if result.deleted_count == 0:
                return "Nothing was deleted"
            else:
                return f"Delete operation was successful ({result.deleted_count})"
        except OperationFailure as err:
            raise err
        finally:
            self.client.close()
            

    def update(self, collection, criteria, params):
        try:
            result = self.client[self.db_name][collection].update_one(criteria, params) 
            if result.matched_count == 0:
                return "Nothing was updated"
            else:
                return f"Update operation was successful ({result.matched_count})"
        except OperationFailure as err:
            raise err
        finally:
            self.client.close()


class RedisDbConnection(AbstractDbConnector):

    __number_of_connections = 0
    __connections = {}

    def __init__(
            self, 
            db_name:str, 
            db_host:str, 
            username:str,
            password:str, 
            port:int):
        """ Constructor.
        """
        super().__init__(db_name, db_host, username, password, port)

        for num_connection, config in RedisDbConnection.__connections.items():
            if config["db_name"] == db_name and config["db_host"] == db_host \
                and config["username"] == username and config["password"] == password \
                and config["port"] == port:
                
                raise Exception("You can't create another RedisDbConnection class")
        RedisDbConnection.__number_of_connections +=1
        RedisDbConnection.__connections[RedisDbConnection.__number_of_connections] \
            = {
                "db_name" : db_name,
                "db_host" : db_host,
                "username" : username,
                "password" : password,
                "port" : port
            }

    def connect(self):
        self.client = Redis(
                        host=self.db_host, 
                        port=self.port,
                        db=int(self.db_name), 
                        username=self.username,
                        password=self.password,
                        decode_responses=True)
        response = self.__check_connection_to_db()  
        return response


    def __check_connection_to_db(self):
        try:
            self.client.ping()
            return "Connection Establish"
        except ConnectionError as err:
            raise(err)


    def insert(self, params, key):
        try:
            if self.client.exists(key) > 0:
                return("This document already has this data")
            else:
                result = self.client.hmset(key, params)
                return result  
        except TimeoutError as err:
            raise err
        except RedisError as err:
            raise err


    def get(self, criteria):
        try:
            result = []
            for key in self.client.keys(criteria):
                result.append(self.client.hgetall(key))
            if not result:
                message = "Nothing was found"
                return message
            else:
                return result
        except TimeoutError as err:
            raise err
        except RedisError as err:
            raise err
        

    def delete(self, criteria):
        try:
            deletes = 0
            for key in self.client.keys(criteria):
                self.client.delete(key)
                deletes += 1
            if deletes == 0:
                message = "Nothing was deleted"
                return message
            else: 
                return "Delete operation was successful"
        except TimeoutError as err:
            raise err
        except RedisError as err:
            raise err
            
    def update(self, criteria, params):
        """Here we can remove this method.
        And instead we can reuse the "delete" and "insert" methods
        to have this behavior
        """
        pass