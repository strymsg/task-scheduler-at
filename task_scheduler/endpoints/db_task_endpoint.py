from flask import Flask, request, jsonify
from flask_restful import Resource, Api, request
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from task_scheduler.tasks.db_task import DbTask
from task_scheduler.task_manager import TaskManager


class DbTaskConnectorSchema(Schema):
    select_db = fields.String(required=True, description="Select database")
    db_name = fields.String(required=True, description="Database name")
    db_host = fields.String(required=True, description="Host name")
    port = fields.Integer(required=True, description="Port to connect")
    password = fields.String(required=True, description="Password credential") 
    username = fields.String(required=True, description="Username credential")


class DbTaskPostRequestSchema(Schema):
    key_id = fields.String(required=True, description="A key to identify the data in the DB")
    config_type = fields.String(required=True, description="Type of configuration")
    query_type = fields.String(required=True, description="Type of query to the DB")
    query = fields.Dict(required=True, description="Data will be insert or update into the DB")
    connector = fields.Nested(DbTaskConnectorSchema)


#  Restful way of creating APIs through Flask Restful
class DbTaskEndpoint(MethodResource, Resource):
    @doc(description='Returns all the data', tags=['DB Task'])
    def get(self):
        """This method represents a GET API method for DB Task endpoint
        """
        configuration = { 
            "key_id": "",
            "query_type" : "GET",
            "config_type" : "Db",
            "query" :  "*",
            "connector": {
                "db_name": "0",
                "db_host": "localhost",
                "username": None,
                "password": None,
                "port" : 6379
            }
        }
        return jsonify(TaskManager().run_dbtask(configuration))

    @doc(description='Creates and updates data into the DB', tags=['DB Task'])
    @use_kwargs(DbTaskPostRequestSchema, location=('json'))
    @marshal_with(schema={},code=400,description="Bad request server didn't understand due to incorrect syntax")
    @marshal_with(schema={},code=401,description="Unauthorized access")  
    @marshal_with(schema={},code=404,description="Data not found") 
    def post(self,**kwargs):
        """This method represents a POST API method for DB Task endpoint
        """
        data = request.get_json()
        configuration = {
            "key_id" : data["key_id"],
            "query_type" : data["query_type"],
            "config_type" : data["config_type"],
            "query" :  data["query"],
            "connector": {
                "db_name": data["connector"]["db_name"],
                "db_host": data["connector"]["db_host"],
                "username": data["connector"]["username"],
                "password": data["connector"]["password"],
                "port" : data["connector"]["port"]
            }
        }
        # connection_db_app.insert(data, key_id)
        return jsonify(TaskManager().run_dbtask(configuration))


class DbTaskEndpointById(MethodResource, Resource):
    @doc(description='Find data by ID', tags=['DB Task'])
    @marshal_with(schema={},code=400,description="Bad request server didn't understand due to incorrect syntax")
    @marshal_with(schema={},code=401,description="Unauthorized access")  
    @marshal_with(schema={},code=404,description="Data not found") 
    def get(self, by_id):
        """This method represents a GET API method for DB Task endpoint by ID
        """
        configuration = {
            "key_id": "", 
            "query_type": "GET",
            "config_type": "Db",
            "query":  f"{by_id}",
            "connector": {
                "db_name": "0",
                "db_host": "localhost",
                "username": None,
                "password": None,
                "port" : 6379
            }
        }
        return jsonify(TaskManager().run_dbtask(configuration))

    @doc(description='Deletes data by ID', tags=['DB Task'])
    @marshal_with(schema={},code=400,description="Bad request server didn't understand due to incorrect syntax")
    @marshal_with(schema={},code=401,description="Unauthorized access")  
    @marshal_with(schema={},code=404,description="Data not found") 
    def delete(self, by_id):
        """This method represents a DELETE API method for DB Task endpoint by ID
        """
        configuration = {
            "key_id": "", 
            "query_type": "DELETE",
            "config_type": "Db",
            "query":  f"{by_id}",
            "connector": {
                "db_name": "0",
                "db_host": "localhost",
                "username": None,
                "password": None,
                "port" : 6379
            }
        }
        return jsonify(TaskManager().run_dbtask(configuration))



