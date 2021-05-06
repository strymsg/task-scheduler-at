from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, request
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from task_scheduler.task_manager import TaskManager


class DbTaskConnectorSchema(Schema):
    db_name = fields.String(required=True, description="Database name")
    db_host = fields.String(required=True, description="Host name")
    port = fields.Integer(required=True, description="Port to connect")
    password = fields.String(required=True, description="Password credential") 
    username = fields.String(required=True, description="Username credential")


class DbTaskConfigurationSchema(Schema):
    key_id = fields.String(required=True, description="A key to identify the data in the DB")
    config_type = fields.String(required=True, description="Type of configuration")
    query_type = fields.String(required=True, description="Type of query to the DB")
    query = fields.Dict(required=True, description="Data will be insert or update into the DB")
    connector = fields.Nested(DbTaskConnectorSchema, required=True)


class DbTaskPostRequestSchema(Schema):
    priority = fields.Integer(required=False, description="Priority value for running the task", default=0)
    configuration = fields.Nested(DbTaskConfigurationSchema, required=True)


#  Restful way of creating APIs through Flask Restful
class DbTaskEndpoint(MethodResource, Resource):
    @doc(description='Insert, update, get and delete data from the RedisDB', tags=['DB Task'])
    @use_kwargs(DbTaskPostRequestSchema, location=('json'))
    @marshal_with(schema={},code=200,description="Request has been successful")  
    @marshal_with(schema={},code=400,description="Bad request server didn't understand due to incorrect syntax")
    @marshal_with(schema={},code=404,description="Data not found") 
    @marshal_with(schema={},code=504,description="The server cannot get a timely response") 
    def post(self,**kwargs):
        """This method represents a POST API method for DB Task endpoint
        """
        try:
            data = request.get_json()
            priority = data["priority"]
            configuration = data["configuration"]
            tm = TaskManager({
                        'type_task': 'Db',
                        'configuration_id': '',
                        'dynamic_configs': configuration,
                        })
            res = tm.execute_dinamically()

        except:
            return make_response(jsonify({
                        'message': 'Task execution finished with errors',
                        'errors': "RedisDB doesn't response: timeout"}), 504)

        else:
            if tm.errors is not None:
                if tm.errors == "Nothing was found" \
                or tm.errors == "Nothing found to delete" \
                or tm.errors == "The data does not exist in the DB":

                    return make_response(jsonify({
                            'message': 'Task execution finished with errors',
                            'errors': tm.errors}), 404)
                else:
                    return make_response(jsonify({
                    'message': 'Task execution finished with errors',
                    'errors': tm.errors}), 400)

            return make_response(jsonify({
                    'message': 'Task execution finished successfully',
                    'results': tm.result, 'errors': '',
                    'task_result_id': res['task_result_id'],
                    'task_id': res['task_id'],
                    'config_id': res['config_id']}), 200)
       




