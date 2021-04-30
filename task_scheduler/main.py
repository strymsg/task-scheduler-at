from task_scheduler import create_app
from task_scheduler.endpoints import api_request_task

app = create_app()
# registering blueprints for api_request_task
app.register_blueprint(api_request_task.bp_tasks)
