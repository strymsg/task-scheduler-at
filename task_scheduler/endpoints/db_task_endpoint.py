from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, request
from task_scheduler.configs.config_redis_db import connection_redis_db
from task_scheduler.tasks.abstract_db_connector import RedisDbConnection
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from task_scheduler.task_manager import TaskManager

redis_db = RedisDbConnection(**connection_redis_db)
redis_db.connect()


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
    @doc(description='Returns all the data', tags=['DB Task'])
    def get(self):
        """This method represents a GET API method for DB Task endpoint
        """
        try:
            result = redis_db.get("*")     
            if result == "Nothing was found":
                return make_response(jsonify({"response": result}), 404)
            return make_response(jsonify({"response": result}), 200)
        except:
            return make_response(jsonify({"response": "RedisDB doesn't response: timeout"}), 504)

    @doc(description='Creates and updates data into the DB', tags=['DB Task'])
    @use_kwargs(DbTaskPostRequestSchema, location=('json'))
    @marshal_with(schema={},code=400,description="Bad request server didn't understand due to incorrect syntax")
    @marshal_with(schema={},code=401,description="Unauthorized access")  
    @marshal_with(schema={},code=404,description="Data not found") 
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
            return make_response(jsonify({"response": "RedisDB doesn't response: timeout"}), 504)

        else:
            if tm.errors is not None:
                return make_response(jsonify({
                'message': 'Task execution finished with errors',
                'task_result_id': res['task_result_id'],
                'config_id': res['config_id'],
                'errors': tm.errors}), 400)

            return make_response(jsonify({
            'message': 'Task execution finished successfully',
            'results': str(tm.result), 'errors': '',
            'task_result_id': res['task_result_id'],
            'config_id': res['config_id']}), 200)
       


class DbTaskEndpointById(MethodResource, Resource):
    @doc(description='Find data by ID', tags=['DB Task'])
    @marshal_with(schema={},code=400,description="Bad request server didn't understand due to incorrect syntax")
    @marshal_with(schema={},code=401,description="Unauthorized access")  
    @marshal_with(schema={},code=404,description="Data not found") 
    def get(self, by_id):
        """This method represents a GET API method for DB Task endpoint by ID
        """
        try:
            result = redis_db.get(f"{by_id}")  
            if result == "Nothing was found":
                return make_response(jsonify({"response": "Not found"}), 404)
            return make_response(jsonify({"response": result}), 200)
        except:
            return make_response(jsonify({"response": "RedisDB doesn't response: timeout"}), 504)

    @doc(description='Deletes data by ID', tags=['DB Task'])
    @marshal_with(schema={},code=400,description="Bad request server didn't understand due to incorrect syntax")
    @marshal_with(schema={},code=401,description="Unauthorized access")  
    @marshal_with(schema={},code=404,description="Data not found") 
    def delete(self, by_id):
        """This method represents a DELETE API method for DB Task endpoint by ID
        """
        try:
            result = redis_db.delete(f"{by_id}") 
            if result == "Nothing was deleted":
                return make_response(jsonify({"response": "Not found"}), 404)
            return make_response(jsonify({"response": result}), 200)
        except:
            return make_response(jsonify({"response": "RedisDB doesn't response: timeout"}), 504)



