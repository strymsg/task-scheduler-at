from task_scheduler.tasks.abstract_db_connector import AbstractDbConnector
from task_scheduler.scheduler.schedule_entry import ScheduledEntry
import schedule


class Scheduler:
    """The main class of the system for running and scheduling tasks.

    ...
    Attributes
    ----------
    scheduled_tasks : Array
        stores all tasks with their scheduled entry to be running
    db_connection: AbstractDbConnector
        connection to database of the system
    
    Methods
    -------
    add_task():
        adds a task to the scheduled tasks
    remove_task():
        removes a task from the scheduled tasks
    edit_task():
        edits a task from the scheduled tasks
    check_executions():
        checks the scheduled tasks that are being executed
    save_task_to_db():
        stores the task into the database
    load_from_db():
        loads the task from the database
    filter_tasks():
        filter tasks
    get_scheduled_entry():
        get the scheduled entry by task ID
    """

    def __init__(self, scheduled_tasks: [], db_connection: AbstractDbConnector):
        self.scheduled_tasks = []
        self.db_connection = db_connection

    def add_task(self, scheduled_entry):
        self.scheduled_tasks.append(scheduled_entry)

    def remove_task(self, filter, task_id: str):
        # TODO
        pass

    def edit_task(self, task_id: str):
        # TODO
        pass

    def check_executions(self):
        # TODO
        pass

    def save_task_to_db(self):
        # TODO
        pass

    def load_from_db(self):
        # TODO
        pass

    def filter_tasks(self):
        # TODO
        pass

    def get_scheduled_entry(self):
        # TODO
        pass