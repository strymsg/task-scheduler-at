from task_scheduler.tasks.abstract_db_connector import MongoDbConnection
from task_scheduler.tasks.config_objects import ConfigFileTask
from task_scheduler.tasks.file_task import FileTask
from bson.objectid import ObjectId


def json_task(task, config_id):
    json_data = {}
    json_data["priority"]=task.priority
    json_data["creation_time"]=task.creation_time
    json_data["type"]=task.type
    json_data["task_results"]=[]
    json_data["task_id"]=task.task_id
    json_data["configs"]=ObjectId(config_id)
    return json_data

args = {
    "location":"testwrite.txt",
    "file_encoding":'utf-8',
    "file_content":'Contenido de pruebas',
    "type":'write',
    "config_type":"File"
}

args2 = {
    "location":"testwrite.txt",
    "file_encoding":'utf-8',
    "file_content":'',
    "type":'read',
    "config_type":"File"
}

config_1 = ConfigFileTask(args)
config_2 = ConfigFileTask(args2)

file_task_1 = FileTask(
                priority=0, 
                config=config_1
                )     

file_task_2 = FileTask(
                priority=0, 
                config=config_2
                )    

connection_db_app = MongoDbConnection(
                        db_name="runtask",
                        db_host="localhost",
                        username=None,
                        password=None, 
                        port=27017)

connection_db_app.connect()

connection_db_app.insert("configs", args)
config_id_1 = connection_db_app.get("configs",args)[0]["_id"]
connection_db_app.get("configs", {"_id":ObjectId(config_id_1)})
connection_db_app.insert("tasks", json_task(file_task_1, config_id_1))

connection_db_app.insert("configs", args2)
config_id_2 = connection_db_app.get("configs",args2)[0]["_id"]
connection_db_app.get("configs", {"_id":ObjectId(config_id_2)})
connection_db_app.insert("tasks", json_task(file_task_2, config_id_2))

