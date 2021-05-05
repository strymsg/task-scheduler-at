from task_scheduler.utils.logger import CustomLogger

from task_scheduler.tasks.abstract_db_connector import MongoDbConnection
from task_scheduler.tasks.config_objects \
    import ConfigFileTask, ConfigApiRequestTask, ConfigDbTask
from task_scheduler.tasks.api_request_task import ApiRequestTask
from task_scheduler.tasks.db_task import AbstractTask, DbTask
from task_scheduler.tasks.file_task import FileTask
from bson.objectid import ObjectId


class TaskManager:
    """
    Class used to execute a specific task with its configuration through the
    RunTask endpoint request.
    ...
    Attributes
    ----------
    params : dict
    params[type_task]: str
        it is the type of the task e.g. "Api-request" or "Db" or "File" to be searched for
    params[configuration_id]: str
        it is the ID of the configuration to be searched for
    db_connection: MongoDbConnection
        the connection has to be passed to the Mongo DB
    Methods
    -------
    execute():
        Executes the task with its configuration
    instantiate():
        Initializes the configuration object and the task object to be executed
    """

    def __init__(self, params, db_connection: MongoDbConnection):
        self.type_task = params["type_task"]
        self.configuration_id = params["configuration_id"]
        self.connection_to_db = db_connection

        self.response = None
        self.errors = None
        self.logger = CustomLogger(__name__)

    def execute(self):
        """
        Executes the task given the configs and saves its results in self object
        :return:
        """
        run_arg = {
            "type": self.type_task,
            "configs": ObjectId(self.configuration_id)
        }
        task_args = self.connection_to_db.get("tasks", run_arg)[0]
        config_args = self.connection_to_db.get(
            "configs",
            {"_id": ObjectId(self.configuration_id)})[0]
        self.instantiate(task_args, config_args)
        try:
            self.response = self.task.sxecute()
            return self.response
        except Exception as e:
            self.errors = str(e)
            self.logger.info(f'Error executing task: {self.errors}')
            return self.errors

    def instantiate(self, task_args, config_args):
        if self.type_task == "Api-request":
            self.config = ConfigApiRequestTask(config_args)
            self.task = ApiRequestTask(
                priority=task_args["priority"],
                config=self.config
            )

        elif self.type_task == "Db":
            self.config = ConfigDbTask(config_args)
            self.task = DbTask(
                priority=task_args["priority"],
                config=self.config
            )

        elif self.type_task == "File":
            self.config = ConfigFileTask(config_args)
            self.task = FileTask(
                priority=task_args["priority"],
                config=self.config
            )