# Task scheduler AT

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
export FLASK_APP=task-scheduler/main.py
export FLASK_ENV=development

# run the flask server
flask run
```

Setup if using pycharm

1. Edit run configuration
2. Add flask config and set the following
3. script path: to venv/bin/flask
4. Parameters: run
5. Envirnoment variables: `FLASK_APP=task_scheduler/main.py; FLASK_ENV=development; FLASK_DEBUG=1`
6. Working directory: root directory of task_scheduler app, for instance: /home/ubuntu/prog102-AT-projects/task-scheduler-at

## Class diagram

[XML](docs/task-manager.xml)

![diagram](docs/task-manager.jpg)

## mongo db schema

The app main database uses mongo. See [docs/Mongo-schema.md](docs/Mongo-schema.md)

