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
    def __init__(self,
                 url, http_method='get', body={}, api_token='', headers={}):
        self.url = url
        self.http_method = http_method
        self.body = body
        self.api_token = api_token
        self.headers = headers
        super().__init__({
            'url': url,
            'http_method': http_method,
            'body': body,
            'api_token': api_token,
            'headers': headers
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
    def __init__(self, location,
                 file_content='', file_encoding='utf-8', type='read'):
        self.location = location
        self.file_content = file_content
        self.file_encoding = file_encoding
        self.type = type
        super().__init__({
            'location': location,
            'file_content': file_content,
            'file_encoding': file_encoding,
            'type': type
        })
