from models import Task
from helpers.errorhelper import ErrorHelper


class FilterTasks:
    def __init__(self, tags=None):
        self.tags = tags
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }

    def filter_tasks(self):
        filtered_tasks = self.get_filtered_tasks()
        if not filtered_tasks:
            no_results_block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "No tasks found with the specified tags."
                }
            }
            self.payload["blocks"].append(no_results_block)
        else:
            for task in filtered_tasks:
                task_block = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Task ID:* {task.task_id}\n*Description:* {task.description}\n"
                                f"*Deadline:* {task.deadline.strftime('%Y-%m-%d')}\n*Points:* {task.points}\n"
                                f"*Tags:* {', '.join(task.tags) if task.tags else 'None'}"
                    }
                }
            self.payload["blocks"].append(task_block)
        return self.payload

    def get_filtered_tasks(self):
        return Task.query.filter(Task.tags.contains(self.tags)).all()
