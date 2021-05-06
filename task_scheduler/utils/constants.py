API_V1 = '/api/v1'
API_ROUTES = {
    'TASKS_ROOT': API_V1 + '/tasks',
    'TASKS': API_V1 + '/tasks',  # GET
    'TASK': API_V1 + '/task/', # GET indivudalmente
    'TASK_API_ADD': API_V1 + '/api-add',         #
    'TASK_API_EXECUTE': API_V1 + '/api-exec',
    'CONFIGS': '/all',
    'CONFIGS_ROOT': API_V1 + '/configs',
    'CONFIG': '/config/',
}

# just for testing
# just for testing (will be removed)
testing_tasks = [
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

## Mongo initial inserts for testing
# db.getCollection('tasks').insert(
#   {
#     "task_id": "task_Api-request_63f1bd71-f441-4519-8a41-33943ccb4dad",
#     "creation_time": "04/27/2021 13:36:35",
#     "priority": 0,
#     "type": "Api-request",
#     "task_results": ["task-result_8c5c74da-8c82-46e0-a338-0bb04979980d"],
#     "config": "config_287575eb-48e5-4598-83f9-d1aeb090effc",
#   }
# )

# db.getCollection('tasks').insert(
#   {
#     "task_id": "task_Api-request_63f1bd71-f441-4519-8a41-33943ccb4dad",
#     "creation_time": "04/27/2021 13:36:35",
#     "priority": 0,
#     "type": "Api-request",
#     "task_results": ["task-result_425c74da-8c82-46e0-9938-0bb04979980d"],
#     "config": "config_eba7877e-a680-4e18-a4ad-ff0073cc822b",
#   }
# )