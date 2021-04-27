from task_scheduler.tasks.abstract_task import AbstractTask
from task_scheduler.tasks.config_objects import ConfigFileTask

class FileTask(AbstractTask):
    def __init__(self, priority, config:ConfigFileTask):
        ''' Instantiates a File task
        :param priority: from 0 (most important) to any greater integer
        :param config(ConfigFileTask): Configuration parameters
        '''
        super().__init__(priority, type='File')
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