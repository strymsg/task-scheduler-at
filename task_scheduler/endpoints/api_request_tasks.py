import json
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource, request
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs

from task_scheduler.tasks.api_request_task import ApiRequestTask, ConfigApiRequestTask
from task_scheduler.tasks.task_manager import TaskManager
from task_scheduler.utils.encoders import JSONEncoder


class ApiRequestExecuteTaskSchema(Schema):
    # task_id = fields.String(required=True, description='A key of a task saved in the scheduler')
    url = fields.String(required=True, description='The URL to do the request')
    http_method = fields.String(required=True, description='The HTTP METHOD for the request')
    headers = fields.Dict(description='Headers of the request')
    body = fields.Dict(description='Request Body (if  exists)')
    api_token = fields.String()


class Resp200Schema(Schema):
    _id = fields.String()
    task_id = fields.String(description='Task id')
    creation_time = fields.String()
    priority = fields.Integer(description='Default to 0 (most important)')
    config = fields.String(description='Configuration id')
    task_results = fields.List(fields.String())
    type = fields.String()

class Resp200ExecSchema(Schema):
    message = fields.String()
    errors = fields.String(default='')
    results = fields.Dict()
    task_result_id = fields.String()
    config_id = fields.String()

class Resp400ExecSchema(Schema):
    errors = fields.String()
    message = fields.String()
    task_result_id = fields.String()
    config_id = fields.String()

class Resp400Schema(Schema):
    message = fields.String(description='Error message')

class ApiRequestTasksEndpoint(MethodResource, Resource):

    @doc(description='Get api request tasks', tags=['API Task'])
    @marshal_with(Resp200Schema,
                  code=200, description='Success getting Api-request tasks')
    @marshal_with(Resp400Schema, code=400, description='Error doing the request')
    @marshal_with(Resp400Schema, code=500, description='Internal error')
    def get(self):
        #return jsonify(testing_tasks)
        # TODO: Define get with filters
        # TODO: Move this query to DB to another class
        try:
            current_app.mongo_connection.connect()
            # TODO: Add filters
            tasks = current_app.mongo_connection.get('tasks', {'type': 'Api-request'})
            #print('....')
            #print(tasks)
            if type(tasks) == str:
                return make_response(jsonify([]), 200)
            return make_response(jsonify(json.loads(JSONEncoder().encode(tasks))), 200)
        except Exception as err:
            # TODO: Log
            print(err)
            return make_response(jsonify({
                "message": f"Error getting tasks"
            }), 500)


class ApiRequestTaskByIdEndpoint(MethodResource, Resource):
    @doc(description="", tags=['API Task'])
    @marshal_with(Resp200Schema,
                  code=200, description='Success getting Api-request tasks')
    @marshal_with(Resp200Schema, code=400, description='Error getting specific task')
    def get(self, task_id):
        # TODO: Move this query to DB to another class
        try:
            current_app.mongo_connection.connect()
            # TODO: Add filters
            tasks = current_app.mongo_connection.get('tasks', {'task_id': task_id})
            if type(tasks) == str:
                return make_response(jsonify([]), 200)
            #print(tasks)
            return make_response(jsonify(json.loads(JSONEncoder().encode(tasks))), 200)
        except Exception as err:
            # TODO: Log
            print(err)
            return make_response(jsonify({
                "message": f"Error getting tasks"
            }), 500)


class ApiRequestTaskExecEndpoint(MethodResource, Resource):
    @doc(description="Execute a task right away", tags=['API Task'])
    @marshal_with(Resp200ExecSchema,
                  code=200, description='Response of executing the given task')
    @marshal_with(Resp400ExecSchema,
                  code=400, description='Error executing the task')
    @use_kwargs(ApiRequestExecuteTaskSchema, location=('json'))
    def post(self, **kwargs):
        '''Method to execute a task and save its results to db'''
        data = request.get_json()

        request_configs = {
            'url': data['url'],
            'http_method': data['http_method'],
            'headers': data['headers'],
            'body': data['body'],
            'api_token': data['api_token']
        }

        tm = TaskManager({
            'type_task': 'Api-request',
            'configuration_id': '',
            'dynamic_configs': request_configs,
        })

        res = tm.run()

        if tm.errors is not None:
            return make_response(jsonify({
                'message': 'Task execution finished with errors',
                'task_result_id': res['task_result_id'],
                'config_id': res['config_id'],
                'errors': tm.errors}), 400)

        return make_response(jsonify({
            'message': 'Task execution finished successfully',
            'results': str(tm.result),
            'errors': '',
            'task_result_id': res['task_result_id'],
            'config_id': res['config_id']}), 200)

# @bp_tasks.route(API_ROUTES['TASK_API_ADD'], methods=('POST', ))
# def add_task():
#     if request.method == 'POST':
#         json_data = request.json
#         # TODO: verify mandatory fields
#         request_task = {
#             'url': json_data['url'],
#             'http_method': json_data['http_method'],
#             'headers': json_data['headers'],
#             'body': json_data['body'],
#             'api_token': json_data['api_token'],
#         }
#         schedule_entry = json_data.get('schedule_entry', {})
#
#         # creating task to add to the scheduler        config = ConfigApiRequestTask(**request_task)
#         print(schedule_entry)
#         config = ConfigApiRequestTask(**request_task)
#         task = ApiRequestTask(0, config=config)
#
#         # TODO: add schedule entry to the scheduler
#         # ...
#         # executing the task (just for testing)
#         try:
#             resp = task.execute()
#             #print(resp)
#             print(resp['json'])
#             return resp['json']
#         except Exception as err:
#             print(f'Error executing task, {err}')
#             return str(err)
