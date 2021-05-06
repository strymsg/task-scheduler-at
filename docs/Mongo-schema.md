# Mongo Schema

```
Scheduler{
    ref: [schedule_entry]
}

schedule_entry {
    ref: task 
}

task {
    ref: config
    ref: task_result
}

config {
}

task_result {
}

```
  - A Scheduler object contains **references** to schedule_entry documents.
  - A schedule_entry **references** to a task.  
  - A task has a **reference** to a config (there exists 3 types of configs), and a task_result.

## Documents

### ScheduleEntry

```json
{
  "schedule_id": "schedule-entry_fd396cc3-3cf6-4e29-af6b-9e48eabffd6b",
  "task_id": "task_Api-request_63f1bd71-f441-4519-8a41-44643ccb4dad",
  "type": "specific",
  "time": "04/26/2021 16:00:00"
}
```

```json
{
  "schedule_id": "schedule-entry_ca11a7c3-5432-477e-99a2-976290ed762b",
  "task_id": "task_Api-request_90b6bd71-6941-1529-8ae1-437643ccb4cac",
  "type": "periodic",
  "every": 15,
  "unit": "minutes"
}
```

### Task

```json
{
  "_id": "ObjectId()",
  "task_id": "task_Api-request_63f1bd71-f441-4519-8a41-44643ccb4dad",
  "creation_time": "04/27/2021 13:35:35",
  "priority": 0,
  "type": "Api-request",
  "config": ObjectID("config_1"),
  "task_results": [ObjectID("taskResult_1"), ObjectID("taskResult_2")],
}
```
### Config

For Api-request

```json
{
  "config_id": "config_1521bd71-f491-89a3-7a41-4462ccb791ad",
  "config_type": "Api-request",
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

```

For Db

```json
{
  "config_id": "config_3391bd81-f491-89a3-7d41-4412ccb79111",
  "key_id": "Config-1",
  "config_type": "Db",
  "query_type": "update",
  "query": {
    "data_aux": "something",
    "note": "something"
  },
  "connector": {
    "db_name": "1",
    "port": 6379,
    "password": "",
    "username": "",
    "db_host": "localhost"
  }
}
```

For file

```json
{
  "config_id": "config_cc91b571-6291-19aa-7db1-2d1273b79190",
  "config_type": "File",
  "location": "nuevo_archivo.txt",
  "file_operation": "write",
  "file_content": "probando contenido...",
  "file_encoding": "utf-8"
}
```

### TaskResult

```json
{
  "task_result_id": "task-result_1234bc71-e29d-89aa-3db1-90c273b7919b",
  "runBy": "user",
  "time": "04/27/2021 14:00:00",
  "error_message": "",
  "result": "status_code: 200"
}
```

### Scheduler

All task documents will be embedding inside a **Scheduler** document:

```json
{
  "schedule_entries": {
    "ApiRequests": [
      ObjectID("schedule-entry_fd396cc3-3cf6-4e29-af6b-9e48eabffd6b")
    ],
    "Db": [
      ObjectID("schedule-entry_ca11a7c3-5432-477e-99a2-976290ed762b")
    ],
    "File": [
      ObjectID("schedule-entry_4b1d17c0-7326-592e-11c2-986290ed762b")
    ]
  }
}
```
