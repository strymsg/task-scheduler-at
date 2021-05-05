# from task_scheduler.main import app
from task_scheduler.utils.constants import API_ROUTES, testing_tasks
from flask import request, jsonify, make_response
from flask_restful import Resource, request
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs

from collections import OrderedDict

from task_scheduler.tasks.api_request_task import ApiRequestTask, ConfigApiRequestTask

class ApiRequestExecuteTaskSchema(Schema):
    #task_id = fields.String(required=True, description='A key of a task saved in the scheduler')
    url = fields.String(required=True, description='The URL to do the request')
    http_method = fields.String(required=True, description='The HTTP METHOD for the request')
    headers = fields.Dict(description='')
    body = fields.Dict(description='Request Body (if exists)')
    #body = fields.from_dict(
    #    {"prop1": fields.Str(), "prop2": fields.Integer(), "anyprop": fields.String()})
    api_token = fields.String()


class ApiRequestTasksEndpoint(MethodResource, Resource):
    @doc(description='', tags=['apirequesttask'])
    def get(self):
        return jsonify(testing_tasks)
    # TODO: Define get with filters


class ApiRequestTaskByIdEndpoint(MethodResource, Resource):
    @doc(description="", tags=['apirequesttask'])
    def get(self, task_id):
        task = {}
        for t in testing_tasks:
            if t['task_id'] == task_id:
                task = t
                break
        if 'task_id' not in task:
            return make_response(jsonify({"message": f"not found {task_id}"}), 404)
        return jsonify(task)


class ApiRequestTaskExecEndpoint(MethodResource, Resource):
    @doc(description="Execute a task right away", tags=['apirequesttask'])
    @use_kwargs(ApiRequestExecuteTaskSchema, location=('json'))
    def post(self, **kwargs):
        '''Method to execute a task and save its results to db'''
        data = request.get_json()
        print('=====================')
        print(data)
        request_task = {
            'url': data['url'],
            'http_method': data['http_method'],
            'headers': data['headers'],
            'body': data['body'],
            'api_token': data['api_token']
        }

        # creating task to execute
        config = ConfigApiRequestTask(**request_task)
        task = ApiRequestTask(0, config=config)

        try:
            resp = task.execute()
            #print(resp)
            print(resp['json'])
            return resp['json']
        except Exception as err:
            print(f'Error executing task, {err}')
            return make_response(jsonify({
                 "message": f"Error executing api-request task, check input: {err}"
            }), 400)


# bp_tasks = Blueprint(
#     'api_request_tasks',
#     __name__,
#     url_prefix=API_ROUTES["TASKS_ROOT"])
#
# # print('FLASK APPPPP', app)
#
# @bp_tasks.route('/hola/', methods=['GET', ])
# def hola():
#     if request.method == 'GET':
#         return 'HOLA!'
#
#
# @bp_tasks.route(API_ROUTES['TASKS'], methods=('GET', ))
# def show_tasks():
#     if request.method == 'GET':
#         return jsonify(testing_tasks)


# @bp_tasks.route(API_ROUTES['TASK'] + '<string:task_id>', methods=('GET', ))
# def show_task(task_id):
#     if request.method == 'GET':
#         # temporary look for specific task
#         task = {}
#         for t in testing_tasks:
#             if t['task_id'] == task_id:
#                 task = t
#                 break
#         if 'task_id' not in task:
#             return make_response(jsonify({"message": f"not found {task_id}"}), 404)
#         return jsonify(task)

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