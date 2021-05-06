import uuid
from task_scheduler.tasks.abstract_db_connector import AbstractDbConnector, RedisDbConnection

class ConfigObject:
    def __init__(self, args={}):
        self.args = args
        # For instance:
        self._config_id = f'config_{uuid.uuid4()}'

    @property
    def config_id(self):
        return self._config_id

    @config_id.setter
    def config_id(self, value):
        self._config_id = value

    def todict(self):
        pass


class ConfigApiRequestTask(ConfigObject):
    def __init__(self, args={}):
        self.url = args["url"]
        self.http_method = args["http_method"]
        self.body = args["body"]
        self.api_token = args["api_token"]
        self.headers = args["headers"]
        super().__init__({
            'url': args["url"],
            'http_method': args["http_method"],
            'body': args["body"],
            'api_token': args["api_token"],
            'headers': args["headers"]
        })

    def todict(self):
        return {
            'config_id': self.config_id,
            'url': self.url,
            'http_method': self.http_method,
            'api_token': self.http_token,
            'headers': self.headers
        }

class ConfigDbTask(ConfigObject):
    def __init__(self, args={}):
        self.key_id = args["key_id"]
        self.query_type = args["query_type"]
        self.query = args["query"]
        self.connector = args["connector"]
        self.db_connection = RedisDbConnection(
                                db_name=self.connector["db_name"], 
                                db_host=self.connector["db_host"], 
                                username=self.connector["username"], 
                                password=self.connector["password"], 
                                port=self.connector["port"]
                                )
        super().__init__({
            'key_id': args["key_id"],
            'query_type': args["query_type"],
            'query': args["query"],
            'connector': {
                'db_name':self.connector["db_name"], 
                'db_host':self.connector["db_host"], 
                'username':self.connector["username"], 
                'password':self.connector["password"], 
                'port':self.connector["port"]
                }
            })


    def todict(self):
        return {
            'config_id': self.config_id,
            'db_name': self.db_connection.db_name,
            'db_host': self.db_connection.db_host,
            'username': self.db_connection.username,
            'password': self.db_connection.password,
            'port': self.db_connection.port,
            'query': self.query
        }



class ConfigFileTask(ConfigObject):
    def __init__(self, location,
                 file_content='', file_encoding='utf-8', file_operation='read'):
        self.location = location
        self.file_content = file_content
        self.file_encoding = file_encoding
        self.file_operation = file_operation
        super().__init__({
            'location': location,
            'file_content': file_content,
            'file_encoding': file_encoding,
            'file_operation': file_operation
        })

    def todict(self):
        return {
            'config_id': self.config_id,
            'location': self.location,
            'file_content': self.file_content,
            'file_encoding': self.file_encoding,
            'file_operation': self.file_operation
            }