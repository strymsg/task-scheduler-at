from abc import abstractmethod
from pymongo import MongoClient
from redis import Redis
from pymongo.errors import ServerSelectionTimeoutError, \
    AutoReconnect, ConnectionFailure, ConfigurationError, OperationFailure
from redis.exceptions import ConnectionError 

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

    
    # def insert(self, params):
    #     self.__check_connection_to_db()
    #     if self.client[self.db_name].count_documents(params, limit = 1):
    #         return("This document already has this data") 
    #     else:
    #         result = self.client[self.db_name].collection1.insert_many([params])
    #         return result.acknowledged


    def insert(self, collection, params):
        ''' Inserts the given params to the collection to the db
        :returns: pymongo result.acknowledged
        '''
        self.__check_connection_to_db()
        if self.client[self.db_name].count_documents(params, limit = 1):
            return (f'The {collection} document has already this data')
        else:
            result = self.client[self.db_name][collection].insert(params)
            return result.acknowledged


    def get(self, criteria):
        self.__check_connection_to_db()
        result = self.client[self.db_name].collection1.find(criteria)
        for collection in result:
            collection.pop("_id")
        return(collection)


    def delete(self, criteria):
        self.__check_connection_to_db()
        result = self.client[self.db_name].collection1.delete_one(criteria) 
        return(result.deleted_count)

            
    def update(self, criteria, params):
        self.__check_connection_to_db()
        result = self.client[self.db_name].collection1.update_one(criteria, params) 
        return(result.matched_count)


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
        self.__check_connection_to_db()
        if self.client.exists(key) > 0:
            return("This document already has this data")
        else:
            result = self.client.hmset(key, params)
            return result  # True


    def get(self, criteria):
        self.__check_connection_to_db()
        result = self.client.hgetall(criteria)
        if not result:
            message = "Nothing was found"
            return message
        return result

        
    def delete(self, criteria):
        self.__check_connection_to_db()
        result = self.client.delete(criteria)
        if result == 0:
            message = "Nothing was deleted"
            return message
        return "Delete operation was successful"

            
    def update(self, criteria, params):
        """Here we can remove this method.
        And instead we can reuse the "delete" and "insert" methods
        to have this behavior
        """
        pass
