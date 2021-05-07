from task_scheduler.tasks.abstract_task import AbstractTask
from task_scheduler.tasks.config_objects import ConfigFileTask

class FileTask(AbstractTask):
    def __init__(self, priority, config: ConfigFileTask):
        ''' Instantiates a File task
        :param priority: from 0 (most important) to any greater integer
        :param config(ConfigFileTask): Configuration parameters
        '''
        super().__init__(priority, type='File')
        self.config = config

    def read_file(self):
        '''Reads the file in the config.location
         and returns it's contents. Raises exception if error occurs
        '''
        try:
            with open(self.config.location, encoding=self.config.file_encoding) as f:
                return f.read()
        except Exception as err:
            # TODO: Log
            raise err

    def write_file(self):
        '''Writes to the config.location using the content in config.file_content
        and config.file_enconding encoding. Raises exception if error occurs
        '''
        try:
            with open(self.config.location,
                      encoding=self.config.file_encoding, mode='w') as f:
                f.write(self.config.file_content)
        except Exception as err:
            # TODO: Log
            raise err

    def execute(self):
        if self.config.file_operation.lower() == 'write':
            try:
                self.write_file()
            except Exception as err:
                # TODO: log
                raise err
        elif self.config.file_operation.lower() == 'read':
            try:
                return self.read_file()
            except Exception as err:
                # TODO: log
                raise err
