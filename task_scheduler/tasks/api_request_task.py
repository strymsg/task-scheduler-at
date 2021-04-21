from task_scheduler.tasks.abstract_task import AbstractTask
from task_scheduler.tasks.config_objects import ConfigApiRequestTask

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