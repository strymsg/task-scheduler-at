import uuid
from task_scheduler.tasks.abstract_task import AbstractTask


class ScheduledEntry:
    """This class assign a schedule entry to a task

    ...
    Attributes
    ----------
    task : AbstractTask
        Link the task with a scheduler entry
    scheduled_id : str
        ID to identify the schedule entry
    
    Methods
    -------
    edit():
        edits a scheduled entry
    """

    def __init__(self, task: AbstractTask):
        self.task = task
        self.scheduled_id = f'schedule-entry_{uuid.uuid4()}'

    def edit(self):
        # TODO
        pass


class SpecificSchedule(ScheduledEntry):
    """This class assign a specific type schedule entry to a task

    ...
    Attributes
    ----------
    task : AbstractTask
        Link the task with a scheduler entry
    time : str
        specific time to which the task will be executed
    type : str
        set to "specific" schedule entry
    
    Methods
    -------
    edit():
        edits a scheduled entry
    """

    def __init__(self, task: AbstractTask, time: str):
        self.time = time
        self.type = "specific"
        super().__init__(task)

    def edit(self):
        # TODO
        pass


class PeriodicSchedule(ScheduledEntry):
    """This class assign a periodic type schedule entry to a task

    ...
    Attributes
    ----------
    task : AbstractTask
        Link the task with a scheduler entry
    every : int
        number to indicate that the task will be executed at specified interval
    unit : str
        unit of time to which the task will be executed
    type : str
        set to "periodic" schedule entry
    
    Methods
    -------
    edit():
        edits a scheduled entry
    """

    def __init__(self, task: AbstractTask, every: int, unit: str):
        self.every = every
        self.unit = unit
        self.type = "periodic"
        super().__init__(task)

    def edit(self):
        # TODO
        pass