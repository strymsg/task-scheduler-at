from flask import Flask
from flask_restful import Resource, Api, reqparse
from task_scheduler.tasks.abstract_db_connector import MongoDbConnection
from task_scheduler.tasks.file_task import FileTask
from task_scheduler.task_manager import TaskManager
import json
from bson import json_util
from bson.json_util import DEFAULT_JSON_OPTIONS
DEFAULT_JSON_OPTIONS.datetime_representation = 2

connection_db_app = MongoDbConnection(
                        db_name="runtask",
                        db_host="localhost",
                        username=None,
                        password=None, 
                        port=27017)
connection_db_app.connect()

app = Flask(__name__)
api = Api(app)

class RunTask(Resource):
    def get(self):
        data = connection_db_app.get("tasks",{})
        
        return json.loads(json_util.dumps(data))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "type_task",
            type=str,
            required=True,
            help="This field is necessary",
        )
        parser.add_argument(
            "configuration_id",
            type=str,
            required=True,
            help="This field is necessary"
        )
        params = parser.parse_args()
        run_task = TaskManager(params, connection_db_app)
        return run_task.execute()


api.add_resource(RunTask, '/api/v1/run/')

app.run(port=5000)