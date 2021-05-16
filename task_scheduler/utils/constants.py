API_VERSION = '/api/v1'

API_ROUTES = {
    'DB_TASK': API_VERSION + '/tasks/db-task',
    'TASKS_BY_ID': API_VERSION + '/tasks/<string:by_id>',
    'TASKS_BY_TYPE': API_VERSION + '/tasks/<string:by_type>',
    'API_TASK_ALL': API_VERSION + '/task/api-task/all',
    'API_TASK': API_VERSION + '/task/api-task',
    'API_TASK_ADD': API_VERSION + '/task/api-task/add',
    'API_TASK_EXECUTE':  API_VERSION + '/task/api-task/exec',
    'ALL_CONFIGS': API_VERSION + '/configs',
}

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
#
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