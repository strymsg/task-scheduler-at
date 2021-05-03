from flask import Flask, request
from flask_restful import Resource, Api, request
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from task_scheduler.tasks.abstract_db_connector import RedisDbConnection

connection_db_app = RedisDbConnection(
                        db_name="0",
                        db_host="localhost",
                        username=None,
                        password=None, 
                        port=6379)

connection_db_app.connect()


class DbTaskPostRequestSchema(Schema):
    key_id = fields.String(required=True, description="A key to identify the data in the DB")
    config = fields.String(required=False, description="A key to identify the data in the DB")
    operation = fields.String(required=False, description="A key to identify the data in the DB")


class DbTaskPutRequestSchema(Schema):
    key_id = fields.String(required=True, description="A key to identify the data in the DB")


#  Restful way of creating APIs through Flask Restful
class DbTaskEndpoint(MethodResource, Resource):
    @doc(description='', tags=['dbtask'])
    # @marshal_with(AwesomeResponseSchema)  # marshalling
    def get(self):
        '''
        Get method represents a GET API method
        '''
        return connection_db_app.get("*")

    @doc(description='', tags=['dbtask'])
    @use_kwargs(DbTaskPostRequestSchema, location=('json'))
    # @marshal_with(AwesomeResponseSchema)  # marshalling 
    def post(self,**kwargs):
        '''
        Get method represents a GET API method
        '''
        data = request.get_json()
        key_id = data.pop("key_id")
        connection_db_app.insert(data, key_id)
        return {'Message': 'Successfully saved'}

    @doc(description='', tags=['dbtask'])
    @use_kwargs(DbTaskPutRequestSchema, location=('json'))
    def put(self):
        '''
        Get method represents a GET API method
        '''
        data = request.get_json()
        key_id = data.pop("key_id")
        result = connection_db_app.update(data, key_id)
        return {'Message': f"{result}"}


# class DbTaskByIdGetRequestSchema(Schema):
#     api_type = fields.String(required=True, description="API type of awesome API")
#     db_type = fields.Integer(required=True, description="API type of awesome API")


# class DbTaskByIdDeleteRequestSchema(Schema):
#     api_type = fields.String(required=True, description="API type of awesome API")
#     db_type = fields.Integer(required=True, description="API type of awesome API")


class DbTaskEndpointById(MethodResource, Resource):
    @doc(description='', tags=['dbtask'])
    # @use_kwargs(DbTaskByIdGetRequestSchema, location=('json'))
    def get(self, by_id):
        '''
        Get method represents a GET API method
        '''
        return connection_db_app.get(f"{by_id}")

    @doc(description='', tags=['dbtask'])
    # @use_kwargs(DbTaskByIdDeleteRequestSchema, location=('json'))
    # @marshal_with(AwesomeResponseSchema)  # marshalling 
    def delete(self, by_id):
        '''
        Get method represents a GET API method
        '''
        return connection_db_app.delete(f"{by_id}")



