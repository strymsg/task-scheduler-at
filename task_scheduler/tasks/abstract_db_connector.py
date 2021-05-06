from abc import abstractmethod
from pymongo import MongoClient
from redis import Redis
from pymongo.errors import (
    ServerSelectionTimeoutError,
    AutoReconnect,
    ConnectionFailure,
    ConfigurationError,
    OperationFailure,
)
from redis.exceptions import ConnectionError, TimeoutError, RedisError
from task_scheduler.utils.exceptions import DbErrorHandler
from task_scheduler.utils.logger import CustomLogger


class AbstractDbConnector:
    """
    Abstract class used to defind databases connections behaviour

    Attributes
    ----------
    db_name : str
        name used to connect to a specific database
    db_host : str
        the localhost used to connect to the database
    username : str
        the username credential used to access to the database
    password : str
        the password credential used to access to the database
    port : int
        port to which it will connect to the database

    Methods
    -------
    connect():
        Tries to connect to the DB and returns a response
    insert():
        Inserts a given data in a specific table into the DB.
    get():
        Inserts a given data in a specific table into the DB.
    delete():
        Deletes a given data in a specific table into the DB.
    update():
        Updates a given data in a specific table into the DB.
    """

    def __init__(
        self, db_name: str, db_host: str, username: str, password: str, port: int
    ):

        self.db_name = db_name
        self.db_host = db_host
        self.username = username
        self.password = password
        self.port = port
        self.logger = CustomLogger(__name__)

        self.logger = CustomLogger(__name__)

    def connect(self):
        pass

    @abstractmethod
    def insert(self, params):
        pass

    @abstractmethod
    def get(self, params):
        pass

    @abstractmethod
    def delete(self, params):
        pass

    @abstractmethod
    def update(self, params):
        pass
 

class MongoDbConnection(AbstractDbConnector):
    """Class used to defined all the requested operations to Mongo DB
    It is not allowed to instantiate twice using the same username, password and port
    it that case it logs an error and returns the former created connection

    Attributes
    ----------
    db_name : str
        name used to connect to a specific database
    db_host : str
        the localhost used to connect to the database
    username : str
        the username credential used to access to the database
    password : str
        the password credential used to access to the database
    port : int
        port to which it will connect to the database

    Methods
    -------
    __check_connection_to_db():
        Verifies the connection to the DB. 
    connect():
        Tries to connect to the DB and returns a response
    insert():
        Inserts a given data in a specific "collection" into the DB.
    get():
        Get a given data in a specific "collection", acoording to a specific "criteria".
    delete():
        Deletes a given data in a specific "collection", acoording to a specific "criteria".
    update():
        Updates a given data in a specific "collection", acoording to a specific "criteria".
    """

    __number_of_connections = 0
    __connections = {}

    def __init__(
            self, 
            db_name: str, 
            db_host: str, 
            username: str,
            password: str, 
            port:int):
        """ Constructor."""

        super().__init__(db_name, db_host, username, password, port)

        for num_connection, config in MongoDbConnection.__connections.items():
            if config["db_name"] == db_name and config["db_host"] == db_host \
                    and config["username"] == username and config["password"] == password \
                    and config["port"] == port:
                error = f'''You can't create another MongoDbConnection class using same configs:
                username: {username}; port: {port}; password
                '''
                self.logger.error(error)
                raise Exception("You can't create another MongoDbConnection class")
        MongoDbConnection.__number_of_connections += 1
        MongoDbConnection.__connections[MongoDbConnection.__number_of_connections] \
            = {
            "db_name": db_name,
            "db_host": db_host,
            "username": username,
            "password": password,
            "port": port
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
            raise (err)
            
    def insert(self, collection, params):
        try:
            if self.client[self.db_name][collection].count_documents(params, limit=1):
                return ("This document already has this data") 
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
    """Class used to defind all the requested operations to Redis DB

    Attributes
    ----------
    db_name : str
        name used to connect to a specific database
    db_host : str
        the localhost used to connect to the database
    username : str
        the username credential used to access to the database
    password : str
        the password credential used to access to the database
    port : int
        port to which it will connect to the database

    Methods
    -------
    __check_connection_to_db():
        Verifies the connection to the DB. 
    connect():
        Tries to connect to the DB and returns a response
    insert():
        Inserts a given data in a specific "key" into the DB.
    get():
        Get data from the DB, acoording to a specific "criteria".
    delete():
        Deletes data in the DB, acoording to a specific "criteria".
    update():
        Updates a given data in the DB, acoording to a specific "criteria".
    """ 

    __number_of_connections = 0
    __connections = {}

    def __init__(
            self,
            db_name: str,
            db_host: str,
            username: str,
            password: str,
            port: int):
        """ Constructor.
        """
        super().__init__(db_name, db_host, username, password, port)
        instance = None
        for num_connection, config in RedisDbConnection.__connections.items():
            if config["db_name"] == db_name and config["db_host"] == db_host \
                    and config["username"] == username and config["password"] == password \
                    and config["port"] == port:
                instance = config["instance"]

        if not instance:
            RedisDbConnection.__number_of_connections += 1
            RedisDbConnection.__connections[RedisDbConnection.__number_of_connections] \
                = {
                "db_name": db_name,
                "db_host": db_host,
                "username": username,
                "password": password,
                "port": port,
                "instance": self
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
            return "Connection Established"
        except ConnectionError as err:
            self.logger.error("Connection could not be established")
            raise DbErrorHandler("Connection could not be established")
 
    def insert(self, params, key):
        try:
            if self.client.exists(key) > 0:
                raise DbErrorHandler("This document already has this data")
            else:
                result = self.client.hmset(key, params)
                return "Data successfully created"  
        except TimeoutError as err:
            self.logger.error("RedisDB doesn't response: timeout")
            raise DbErrorHandler("RedisDB doesn't response: timeout")
        except RedisError as err:
            self.logger.error("RedisDB cannot process the query")
            raise DbErrorHandler("RedisDB cannot process the query")

    def get(self, criteria):
        try:
            result = {}
            for key in self.client.keys(criteria):
                result[key] = self.client.hgetall(key)
            if not result:
                raise DbErrorHandler("Nothing was found")
            else:
                return result
        except TimeoutError as err:
            self.logger.error("RedisDB doesn't response: timeout")
            raise DbErrorHandler("RedisDB doesn't response: timeout")
        except RedisError as err:
            self.logger.error("RedisDB cannot process the query")
            raise DbErrorHandler("RedisDB cannot process the query")

    def delete(self, criteria):
        try:
            deletes = 0
            for key in self.client.keys(criteria):
                self.client.delete(key)
                deletes += 1
            if deletes == 0:
                raise DbErrorHandler("Nothing found to delete")
            else: 
                return "Delete operation was successful"
        except TimeoutError as err:
            self.logger.error("RedisDB doesn't response: timeout")
            raise DbErrorHandler("RedisDB doesn't response: timeout")
        except RedisError as err:
            self.logger.error("RedisDB cannot process the query")
            raise DbErrorHandler("RedisDB cannot process the query")

    def update(self, criteria, params):
        """Here we can remove this method.
        And instead we can reuse the "delete" and "insert" methods
        to have this behavior
        """
        pass

        try:
            deletes = 0
            for key in self.client.keys(criteria):
                self.client.delete(key)
                deletes += 1
            if deletes == 0:
                raise DbErrorHandler("The data does not exist in the DB")
            else: 
                result = self.client.hmset(criteria, params)
                return "Successfully updated"
        except TimeoutError as err:
            self.logger.error("RedisDB doesn't response: timeout")
            raise DbErrorHandler("RedisDB doesn't response: timeout")
        except RedisError as err:
            self.logger.error("RedisDB cannot process the query")
            raise DbErrorHandler("RedisDB cannot process the query")