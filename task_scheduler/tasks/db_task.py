from task_scheduler.tasks.abstract_task import AbstractTask
from task_scheduler.tasks.config_objects import ConfigDbTask

class DbTask(AbstractTask):
    def __init__(self, priority, config:ConfigDbTask):
        ''' Instantiates a Database task
        :param priority: from 0 (most important) to any greater integer
        :param config(ConfigDbTask): Configuration parameters
        '''
        super().__init__(priority, type='Db')
        self.config = config
        self.config.db_connection.connect()
 
    def validate(self):
        # TODO: implement validation of data
        pass
 
    # In all of these methods still have to modify the schema for interaction
    # with the Redis database, i.e. add a "key" field in the request.
    #
    # In this case is hard-coded to "key" = "config-" 
    def insert(self):  
        return self.config.db_connection.insert(self.config.query, "config-")
 
    def get(self):
        return self.config.db_connection.get(self.config.query)
 
    def update(self):
        return self.config.db_connection.update(self.config.query)
 
    def delete(self):
        return self.config.db_connection.delete(self.config.query)
 
    def execute(self):
        try:
            self.validate()
        except Exception as err:
            raise err
        else:
            if self.config.query_type.upper() == "INSERT":
                return self.insert()
            elif self.config.query_type.upper() == "GET":
                return self.get()
            elif self.config.query_type.upper() == "UPDATE":
                return self.update()
            elif self.config.query_type.upper() == "DELETE":
                return self.delete()
