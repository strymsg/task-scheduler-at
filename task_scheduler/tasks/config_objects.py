from task_scheduler.tasks.abstract_db_connector import AbstractDbConnector, RedisDbConnection

class ConfigObject:
    def __init__(self, args={}):
        self.args = args
        # TODO: Define how to get the config_id property
        self._config_id = ''

    @property
    def config_id(self):
        return self._config_id

    @config_id.setter
    def config_id(self, value):
        self._config_id = value


class ConfigApiRequestTask(ConfigObject):
    def __init__(self, args={}):
        self.url = args["url"]
        self.http_method = args["http_method"]
        self.body = args["body"]
        self.api_token = args["api_token"]
        self.headers = args["headers"]
        super().__init__({
            'url': args["url"],
            'http_method': rgs["http_method"],
            'body': args["body"],
            'api_token': args["api_token"],
            'headers': args["headers"]
        })


class ConfigDbTask(ConfigObject):
    def __init__(self, query:str, db_connection:AbstractDbConnector):
        self.db_connection = db_connection
        self.query = query
        super().__init__({
            'db_name': self.db_connection.db_name,
            'db_host': self.db_connection.db_host,
            'username': self.db_connection.username,
            'password': self.db_connection.password,
            'port': self.db_connection.port,
            'query': query
        })


class ConfigFileTask(ConfigObject):
    def __init__(self, args={}):
        self.location = args["location"]
        self.file_content = args["file_content"]
        self.file_encoding = args["file_encoding"]
        self.type = args["type"]
        super().__init__({
            'location': args["location"],
            'file_content': args["file_content"],
            'file_encoding': args["file_encoding"],
            'type': args["type"]
        })
