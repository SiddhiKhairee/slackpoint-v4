from models import Task, db
from helpers.errorhelper import ErrorHelper
from sqlalchemy import func
import json


class FilterTasks:
    def __init__(self, tags: list = None):
        """
        Initializes the FilterTasks command with any tags that might be there

        :param tags: The tags that are being filtered for
        :type tags: list
        """
        self.tags = tags
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }

    def filter_tasks(self):
        """
        Filters tasks based on the filters that get added to the system
        """
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
                # Get all task attributes
                task_id = getattr(task, "task_id")
                desc = getattr(task, "description")
                deadline = getattr(task, "deadline").strftime('%Y-%m-%d')
                points = getattr(task, "points")
                tags = getattr(task, "tags")
                task_block = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f">Task ID: {task_id} ({points} SlackPoints) {desc} [Deadline: {deadline}]\n"
                                f">Tags: {', '.join(tags) if tags else 'None'}"
                    }
                }
            self.payload["blocks"].append(task_block)
        return self.payload

    def get_filtered_tasks(self) -> list:
        """
        Queries the database for all tasks with the tag (right now only supports one tag)

        :return: A list containing all the tasks that have the tag
        :rtype: list
        """

        # If tags is empty, return none
        if not self.tags:
            return None

        # Gets all Tasks
        task_list = db.session.query(Task).all()
        task_hits = []

        # Iterate through each task, and each tag to check
        for task in task_list:
            # Gets the tags of the current task
            curr_tags = getattr(task, "tags")
            # If there are no tags, continue
            if not curr_tags:
                continue
            # Iterate and check each tag
            for tag in curr_tags:
                # Iterate through each filter-specified tag
                for param_tag in self.tags:
                    # If the tag is the same, add it to the hit list
                    if tag == param_tag:
                        task_hits.append(task)
                        break

        return task_hits
