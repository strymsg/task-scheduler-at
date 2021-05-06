from task_scheduler.tasks.abstract_task import AbstractTask
from task_scheduler.tasks.config_objects import ConfigDbTask
from task_scheduler.utils.exceptions import ConfigurationError
from task_scheduler.utils.logger import CustomLogger


class DbTask(AbstractTask):
    """This class defines the operations to be performed with a specific DB
    ...
    Attributes
    ----------
    priority : int
        number assigns a level of priority to run the task
    config : ConfigDbTask
        a configuration object containing the parameters nedded to run the task 
    Methods
    -------
    validate():
        Verifies the content of a given data before makes a query to the DB.
    insert():
        Inserts a given data into a specific DB.
    get():
        Get a given data from a specific DB.
    delete():
        Deletes a given data from a specific DB.
    update():
        Updates a given data from a specific DB.
    """
    def __init__(self, priority, config:ConfigDbTask):
        """Instantiates a Database task
        ...
        Attributes
        ----------
        priority : int
            a number from 0 (most important) to any greater integer
        config : ConfigDbTask
            a configuration object containing the parameters nedded to run the task 
        """
        super().__init__(priority, type='Db')
        self.config = config

        self.config.db_connection.connect()
        self.logger = CustomLogger(__name__)

    def insert(self):  
        return self.config.db_connection.insert(self.config.query, self.config.key_id)
 
    def get(self):
        return self.config.db_connection.get(self.config.key_id)
 
    def update(self):
        return self.config.db_connection.update(self.config.key_id, self.config.query)
 
    def delete(self):
        return self.config.db_connection.delete(self.config.key_id)
 
    def execute(self):
        if self.config is None:
            self.logger.error("Need a configuration object to do query to the DB")
            raise  ConfigurationError("Need a configuration object to do query to the DB")
        else:
            if self.config.query_type.upper() == "INSERT":
                return self.insert()
            elif self.config.query_type.upper() == "GET":
                return self.get()
            elif self.config.query_type.upper() == "UPDATE":
                return self.update()
            elif self.config.query_type.upper() == "DELETE":
                return self.delete()