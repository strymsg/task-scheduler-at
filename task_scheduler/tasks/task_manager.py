import json
import uuid
from datetime import datetime as dt
from flask import current_app

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

    def __init__(self, params, db_connection: MongoDbConnection=None,
                 dynamic_configs=None):
        self.type_task = params["type_task"]
        self.configuration_id = params["configuration_id"]
        if db_connection is None:
            self.connection_to_db = current_app.mongo_connection
            # self.connection_to_db = g.db # global db connection
        else:
            self.connection_to_db = db_connection
        self.dynamic_configs = params.get('dynamic_configs', {})

        self.result = None
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
            self.result = self.task.execute()
            return self.result
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

    def execute_dinamically(self):
        """Executes the task and saves its results to the DB.
        It creates a config object and task result to be into Db using self.save_into_db()

        :returns: True if there is no error and False if some error occurs (logs it)
        """
        if self.type_task == "Api-request":
            self.config = ConfigApiRequestTask(**self.dynamic_configs)
            self.task = ApiRequestTask(
                priority=0, # fixed priority
                config=self.config
            )
        elif self.type_task == 'Db':
            # TODO: implement
            pass
        elif self.type_task == 'File':
            # TODO: implement
            pass
        
        try:
            self.result = self.task.execute()
        except Exception as e:
            self.errors = str(e)
            self.logger.info(f'Error executing task: {self.errors}')
            return False
        
        res = self.save_into_db()
        return res

        
    def save_into_db(self):
        '''Saves the task execution results to the DB. Creates both documents
        config and task_results following the schema defined at docs/Mongo-schema.md
        
        :returns: A dict with task_result_id and config_id.
        Empty values if error occurs, errors are logged.
        '''
        config_dbobj = {}
        if self.type_task == "Api-request":
            config_dbobj = {
                #'_id': ObjectId(self.config['config_id']),
                'config_id': self.config.config_id,
                'url': self.config.url,
                'http_method': self.config.http_method,
                'headers': json.dumps(self.config.headers),
                'body': json.dumps(self.config.body),
                'api_token': self.config.api_token
                }
        elif self.type_task == 'Db':
            # TODO: implement
            pass
        elif self.type_task == 'File':
            # TODO: implement
            pass
        
        task_resultdb = {
            "task_result_id": f"task-result_{uuid.uuid4()}",
            "runBy": "user",
            "time": dt.now().strftime('%d/%m/%Y %H:%M:S'),
            "error_message": str(self.errors),
            "result": str(self.result)
            }

        try:
            self.connection_to_db.connect()
            self.connection_to_db.insert('config', config_dbobj)
            self.connection_to_db.insert('task_result', task_resultdb)
            self.logger.info(f'Task execution saved to DB')
            return {
                'task_result_id': task_resultdb['task_result_id'],
                'config_id': config_dbobj['config_id']
            }
        except Exception as err:
            self.logger.error(f'Error registering task results into db: {err}')
            return {'task_result_id': '', 'config_id': ''}