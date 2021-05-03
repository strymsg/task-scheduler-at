# from task_scheduler.main import app
from task_scheduler.utils.constants import API_ROUTES, testing_tasks
from flask import Blueprint, request, jsonify

from task_scheduler.tasks.api_request_task import ApiRequestTask, ConfigApiRequestTask

import json

bp_tasks = Blueprint(
    'api_request_tasks',
    __name__,
    url_prefix=API_ROUTES["TASKS_ROOT"])

# print('FLASK APPPPP', app)

@bp_tasks.route('/hola/', methods=['GET', ])
def hola():
    if request.method == 'GET':
        return 'HOLA!'


@bp_tasks.route(API_ROUTES['TASKS'], methods=('GET', ))
def show_tasks():
    if request.method == 'GET':
        return jsonify(testing_tasks)


@bp_tasks.route(API_ROUTES['TASK'] + '<string:task_id>', methods=('GET', ))
def show_task(task_id):
    if request.method == 'GET':
        # temporary look for specific task
        task = {}
        for t in testing_tasks:
            if t['task_id'] == task_id:
                task = t
                break
        return jsonify(task)


@bp_tasks.route(API_ROUTES['TASK_API_EXECUTE'], methods=('POST',))
def exec_task():
    if request.method == 'POST':
        json_data = request.json
        # TODO: verify mandatory fields
        request_task = {
            'url': json_data['url'],
            'http_method': json_data['http_method'],
            'headers': json_data['headers'],
            'body': json_data['body'],
            'api_token': json_data['api_token']
        }

        # creating task to execute
        config = ConfigApiRequestTask(**request_task)
        task = ApiRequestTask(0, config=config)

        # executing the task
        try:
            resp = task.execute()
            #print(resp)
            print(resp['json'])
            return resp['json']
        except Exception as err:
            print(f'Error executing task, {err}')
            return str(err)

@bp_tasks.route(API_ROUTES['TASK_API_ADD'], methods=('POST', ))
def add_task():
    if request.method == 'POST':
        json_data = request.json
        # TODO: verify mandatory fields
        request_task = {
            'url': json_data['url'],
            'http_method': json_data['http_method'],
            'headers': json_data['headers'],
            'body': json_data['body'],
            'api_token': json_data['api_token'],
        }
        schedule_entry = json_data.get('schedule_entry', {})

        # creating task to add to the scheduler        config = ConfigApiRequestTask(**request_task)
        print(schedule_entry)
        config = ConfigApiRequestTask(**request_task)
        task = ApiRequestTask(0, config=config)

        # TODO: add schedule entry to the scheduler
        # ...
        # executing the task (just for testing)
        try:
            resp = task.execute()
            #print(resp)
            print(resp['json'])
            return resp['json']
        except Exception as err:
            print(f'Error executing task, {err}')
            return str(err)