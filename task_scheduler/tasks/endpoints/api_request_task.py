from task_scheduler.main import app
from task_scheduler.utils.constants import API_ROUTES
import json

print('FLASK APPPPP', app)

# just for testing:
tasks = [
    {
        "task_id": "task_Api-request_63f1bd71-f441-4519-8a41-44643ccb4dad",
        "creation_time": "04/27/2021 13:35:35",
        "priority": 0,
        "type": "Api-request",
        "config": "config_1",
        "task_results": ["taskResult_1"],
        "config_id": "config_1521bd71-f491-89a3-7a41-4462ccb791ad",
        "type": "Api-request",
        "config": {
            "config_id": "config_1521bd71-f491-89a3-7a41-4462ccb791ad",
            "url": "https://reqbin.com/echo/post/json",
            "http_method": "POST",
            "headers": {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            "body": {
                "Id": 78912,
                "Customer": "Jason Sweet",
                "Quantity": 1,
                "Price": 18.00
            },
            "api_token": ""
        }
    },
    {
        "task_id": "task_Api-request_d782bd71-f441-4519-8a41-44643ccb4dad",
        "creation_time": "04/27/2021 13:35:35",
        "priority": 0,
        "type": "Api-request",
        "config": "config_1",
        "task_results": ["taskResult_1"],
        "config_id": "config_1390bd71-f491-89a3-7a41-4462ccb791ad",
        "type": "Api-request",
        "config": {
            "config_id": "config_1390bd71-f491-89a3-7a41-4462ccb791ad",
            "url": "https://api.github.com",
            "http_method": "GET",
            "headers": {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            "body": {},
            "api_token": ""
        }
    },
]

@app.route('/hola/', methods=['GET'])
def hola():
    return 'HOLA!'

@app.route(API_ROUTES['TASKS'], methods=('GET'))
def show_tasks():
    return ('Tasks:', json.dump(tasks))

#@app.route(API_ROUTES['TASK'] + )