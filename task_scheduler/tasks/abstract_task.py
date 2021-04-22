from datetime import datetime
from abc import abstractmethod

class AbstractTask:
    def __init__(self, priority=0, type=''):
        self.priority = priority
        self.creation_time = datetime.now()
        self.type = type
        self.execution_information = None
        # TODO: Define how to get the task_id
        self._task_id = ''

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        self._task_id = value

    @abstractmethod
    def execute(self):
        pass

