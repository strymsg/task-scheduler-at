## Mongo Schema

**ApiRequestTask**:
```json
{
  "_id": "ObjectId()",
  "task_id": "task_Api-request_63f1bd71-f441-4519-8a41-44643ccb4dad_04/27/2021 13:35:35",
  "creation_time": "04/27/2021 13:35:35",
  "priority": 0,
  "type": "Api-request",
  "execution_information": {
    "last_execution": "04/27/2021 14:00:00",
    "executions": [
      {
	"time": "04/27/2021 14:00:00",
	"error_message": "",
	"result": "status_code: 200",
      },
      {
	"time": "04/27/2021 13:45:00",
	"error_message": "Internal server error.",
	"result": "status_code: 500",
      }
    ],
  },
  "config": {
    "url": "https://reqbin.com/echo/post/json",
    "http_method": "POST",
    "headers": { "Accept": "application/json", "Content-Type": "application/json" },
    "body": {
       "Id": 78912,
       "Customer": "Jason Sweet",
       "Quantity": 1,
       "Price": 18.00      
    },
    "api_token": ""
  },
  "schedule": {
    "scheduled_id": "schedule_1521bd71-f491-89a3-7a41-4462ccb791ad_04/27/2021 13:35:35",
    "type": "periodic",
    "every": 15,
    "unit": "minutes"
  }
}
```
**ConfigFileTask**:
```json
{
  "_id": "ObjectId()",
  "task_id": "task_File_12f1bd71-f441-4519-8a41-44643ccb4def_04/26/2021 13:35:35",
  "creation_time": "04/27/2021 13:35:35",
  "priority": 0,
  "type": "File",
  "execution_information": {
    "last_execution": "04/26/2021 16:00:00",
    "executions": [
      {
	"time": "04/26/2021 16:00:00",
	"error_message": "",
	"result": "done.",
      },
    ],
  },
  "config": {
    "location": "nuevo_archivo.txt",
    "type": "write",
    "file_content": "probando contenido...",
    "file_encoding": "utf-8"
  },
  "schedule": {
    "scheduled_id": "schedule_e921bd71-b491-19a3-ba4d-7492ccb79180_04/26/2021 13:35:35",
    "type": "specific",
    "time": "04/26/2021 16:00:00"
  }
}
```
**DbTask**:
```json
{
  "_id": "ObjectId()",
  "task_id": "task_Db_63f1bd88-f44c-2519-8a41-44643ccb4c4c_04/27/2021 13:35:35",
  "creation_time": "04/27/2021 12:35:35",
  "priority": 0,
  "type": "File",
  "execution_information": {
    "last_execution": "04/26/2021 16:00:00",
    "executions": [
      {
	"time": "04/26/2021 16:00:00",
	"error_message": "",
	"result": "Ok.",
      },
      {
	"time": "04/26/2021 12:00:00",
	"error_message": "Reference error....",
	"result": "Reference error....",
      },
    ],
  },
  "config": {
    "type": "update",
    "query": "HSET clave1 nuevovalor",
    "connector": {
      "db_name": "1",
      "port": 6379,
      "password": "",
      "username": "",
      "db_host": "localhost"
    }
  },
  "schedule": {
    "scheduled_id": "schedule_aa21bd71-e491-18c5-ba59-7492ccb79180_04/26/2021 13:35:35",
    "type": "periodic",
    "every": 12,
    "unit": "hours"
  }
}
```
All task documents will be embedding inside a **Scheduler** document:

```json
{
  "db_connection": {
    "db_name": "task_scheduler",
    "port": 21017,
    "password": "",
    "username": "",
    "db_host": "localhost"
  },
  tasks: [
    ObjectID("task_Api-request_63f1bd71-f441-4519-8a41-44643ccb4dad_04/27/2021 13:35:35"),
    ObjectID("task_File_12f1bd71-f441-4519-8a41-44643ccb4def_04/26/2021 13:35:35"),
    ObjectID("task_Db_63f1bd88-f44c-2519-8a41-44643ccb4c4c_04/27/2021 13:35:35"
  ]
}
```