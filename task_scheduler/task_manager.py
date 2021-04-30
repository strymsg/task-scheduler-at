from task_scheduler.tasks.abstract_db_connector import MongoDbConnection
from task_scheduler.tasks.config_objects \
                import ConfigFileTask, ConfigApiRequestTask, ConfigDbTask
from task_scheduler.tasks.api_request_task import ApiRequestTask
from task_scheduler.tasks.db_task import DbTask
from task_scheduler.tasks.file_task import FileTask
from bson.objectid import ObjectId

class TaskManager:

    def __init__(self, params, db_connection: MongoDbConnection):
        self.type_task = params["type_task"]
        self.configuration_id = params["configuration_id"]
        self.connection_to_db = db_connection

    def execute(self):
        run_arg = {
            "type": self.type_task,
            "configs": ObjectId(self.configuration_id)
        }
        task_args = self.connection_to_db.get("tasks", run_arg)[0]
        config_args = self.connection_to_db.get("configs", {"_id":ObjectId(self.configuration_id)})[0]
        self.instantiate(task_args, config_args)
        self.task.execute()
        
        return "SUCCESS"

    def instantiate(self, task_args, config_args):
        if self.type_task == "Api-request":
            pass
        elif self.type_task == "Db":
            pass
        elif self.type_task == "File":
            self.config = ConfigFileTask(config_args)
            self.task = FileTask(
                            priority=task_args["priority"],
                            config=self.config
                            )

