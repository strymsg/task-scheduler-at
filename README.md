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

## Class diagram

[XML](docs/task-manager.xml)

![diagram](docs/task-manager.jpg)

## mongo db schema

The app main database uses mongo. See [docs/Mongo-schema.md](docs/Mongo-schema.md)