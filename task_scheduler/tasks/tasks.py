from datetime import datetime

from task_scheduler.tasks.config_objects import \
    ConfigApiRequestTask, ConfigDbTask, ConfigFileTask

class AbstractTask:
    def __init__(self, priority=0, type=''):
        self.priority = priority
        self.creation_time = datetime.now()
        self.type = type
        self.execution_information = None
        # TODO: Define how to get the task_id
        self._task_id = ''

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        self._task_id = value

    def execute(self):
        '''this method should be implemented'''
        pass

class ApiRequestTask(AbstractTask):
    def __init__(self, priority, config:ConfigApiRequestTask):
        ''' Instantiates an Api request task
        :param priority: from 0 (most important) to any greater integer
        :param config(ConfigApiRequestTask): Configuration parameters
        '''
        super().__init__(priority, type='Api-request')
        self.config = config

    def do_request(self):
        # TODO: implement the request with the config
        pass

    def execute(self):
        # TODO: do some verification if needed
        self.do_request()

class DbTask(AbstractTask):
    def __init__(self, priority, config:ConfigDbTask):
        ''' Instantiates a Database task
        :param priority: from 0 (most important) to any greater integer
        :param config(ConfigDbTask): Configuration parameters
        '''
        super().__init__(priority, type='Db-task')
        self.config = config

    def request_to_db(self):
        # TODO: implement the request to the db
        pass

    def save_into_db(self):
        # TODO: Implement
        pass

class FileTask(AbstractTask):
    def __init__(self, priority, config:ConfigFileTask):
        ''' Instantiates a File task
        :param priority: from 0 (most important) to any greater integer
        :param config(ConfigFileTask): Configuration parameters
        '''
        super().__init__(preiority, type='File-task')
        self.config = config

    def read_file(self):
        # TODO: implement
        pass

    def write_file(self):
        # TODO: implement
        pass

    def execute(self):
        # TODO: implement
        pass