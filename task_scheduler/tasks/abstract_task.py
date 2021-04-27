import uuid
from datetime import datetime
from abc import abstractmethod

class AbstractTask:
    def __init__(self, priority=0, type=''):
        self.priority = priority
        self.creation_time = datetime.now()
        self.type = type
        self.execution_information = None

        # For instance:
        # task_Api-request_63f1bd71-f441-4519-8a41-44643ccb4dad_04/27/2021 13:35:35
        self._task_id = \
            f'task_{type}_{uuid.uuid4()}_{self.creation_time.strftime("%m/%d/%Y %H:%M:%S")}'

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        self._task_id = value

    @abstractmethod
    def execute(self):
        pass

