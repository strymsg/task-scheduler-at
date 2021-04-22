from abc import abstractmethod

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

    def __init__(
            self, 
            db_name:str, 
            db_host:str='localhost', 
            username:str='admin',
            password:str='admin', 
            port:int=27017):
        
        super().__init__(db_name, db_host, username, password, port)

    def connect(self):
        # TODO: implement insert method to the dbs
        pass

    
    def insert(self, params):
        # TODO: implement insert method to the dbs
        pass

    
    def delete(self, params):
        # TODO: implement insert method to the dbs
        pass
    
    def update(self, params):
        # TODO: implement insert method to the dbs
        pass      


class RedisDbConnection(AbstractDbConnector):

    def __init__(
            self, 
            db_name:str, 
            db_host:str='localhost', 
            username:str='admin',
            password:str='admin', 
            port:int=27017):
        
        super().__init__(db_name, db_host, username, password, port)

    def connect(self):
        # TODO: implement insert method to the dbs
        pass
    
    def insert(self, params):
        # TODO: implement insert method to the dbs
        pass
    
    def delete(self, params):
        # TODO: implement insert method to the dbs
        pass
    
    def update(self, params):
        # TODO: implement insert method to the dbs
        pass      