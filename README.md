# Task scheduler AT
## Problem

So practically want we want to do is a Task Manager.
 
1. In which we are going to have 3 different types of **tasks** to request/send data:
  * API:
    - request information using a url
    - send data to a post url
  * DB:
    - Requests information from a db
    - Save information into a specific db
  * Files:
    - Get the file from a directory or an url and reading its content
    - Create a file and save it into a directory or send it to a url
2. The tasks defined above can be executed with different arguments, so there should be **configuration objects** that can be reused by those tasks, those configuration objects can contain different arguments like the URL, or db query, file dir/url or others.
3. Every task  execution information should be saved: which configuration was used, which tasks was run, time at which the task was run along with the result
4. Tasks can be scheduled
   - There are 2 types of scheduler entries, frequency(every n secs) and crontab(defining specific time)
   - The **scheduler entries** information should be saved into a DB, but there is also the possibility of running a scheduler without having a db
5. And more details about what I want as a user:
   - As a user I can ask for:
      1. All the tasks I have
      2. Tasks by id
      3. All the tasks I have filter by type(api, db, files)
      4. All the tasks I have based on a time of period
      5. All the configuration I have
      6. All the schedulers entries I have
   - As a user I can ask to:
      1. Schedule tasks every task schedule is scheduler entry
      2. Edit a schedule ?
      3. Run a task
      4. Save/Edit Configurations
   - As a user I can ask to delete:
      1. Tasks by type
      2. Tasks by id
      3. Tasks run in a period of time
      4. Configurations that are not used by any tasks
      5. All Scheduler entries
      6. Scheduler entry by id

## Install

```bash
# create virtualenv
virtualenv --python=python3

# activate the virtualenv
. venv/bin/activate

# install requirements
pip install -r requirements.txt
pip install -r requirements.dev.txt
```
Setup and run the application
```
export FLASK_APP=main.py
export FLASK_ENV=development

# run the flask development server
flask run
```

Setup if using pycharm

1. Edit run configuration
2. Add flask config and set the following
3. script path: to venv/bin/flask
4. Parameters: run
5. Envirnoment variables: `FLASK_APP=main.py; FLASK_ENV=development; FLASK_DEBUG=1`
6. Working directory: root directory of task_scheduler app, for instance: /home/ubuntu/prog102-AT-projects/task-scheduler-at

## Class diagram

[XML](docs/task-manager.xml)

![diagram](docs/task-manager.jpg)

## mongo db schema

The app main database uses mongo. See [docs/Mongo-schema.md](docs/Mongo-schema.md)

### Execute tests

```
# with virtualenvironment activated
pip3 install tox
# execute
tox
```