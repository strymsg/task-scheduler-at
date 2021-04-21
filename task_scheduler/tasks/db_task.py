from task_scheduler.tasks.abstract_task import AbstractTask
from task_scheduler.tasks.config_objects import ConfigDbTask

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