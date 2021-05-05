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
            'http_method': args["http_method"],
            'body': args["body"],
            'api_token': args["api_token"],
            'headers': args["headers"]
        })


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