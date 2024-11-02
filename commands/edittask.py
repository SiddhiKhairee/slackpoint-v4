from copy import deepcopy
import random
from models import *
from datetime import date
from helpers.errorhelper import ErrorHelper


class EditTask:
    """
    This class handles the Edit Task functionality.
    """

    base_edit_task_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">{greeting}! Your task SP-{id} was edited successfully.",
        },
    }

    greetings = ["Awesome", "Great", "Congratulations", "Well done", "Let's go"]

    def __init__(self, task_id=None):
        """
        Constructor to initialize payload object

        :param:
        :type:
        :raise:
        :return: None
        :rtype: None

        """
        self.task_id = task_id
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }

    def edit_task_input_blocks(self):
        """
        Edit blocks list containing input fields for description, deadline, points of a task, along with a button to edit the task

        :param:
        :type:
        :raise:
        :return: Blocks list
        :rtype: list

        """
        task = self.get_task()
        block_description = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "edit_action_description",
                "initial_value": task.description
            },
            "label": {"type": "plain_text", "text": "Description", "emoji": True},
        }
        block_tags = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_action_tags",
                "initial_value": task.tags
            },
            "label": {"type": "plain_text", "text": "Tag", "emoji": True},
        }
        block_deadline = {
            "type": "input",
            "element": {
                "type": "datepicker",
                "initial_date": task.deadline.strftime("%Y-%m-%d"),
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": True,
                },
                "action_id": "edit_action_deadline",
            },
            "label": {"type": "plain_text", "text": "Deadline", "emoji": True},
        }
        block_points = {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {"type": "plain_text", "text": "Select", "emoji": True},
                "options": [
                    {
                        "text": {"type": "plain_text", "text": "1", "emoji": False},
                        "value": "1",
                    },
                    {
                        "text": {"type": "plain_text", "text": "2", "emoji": False},
                        "value": "2",
                    },
                    {
                        "text": {"type": "plain_text", "text": "3", "emoji": False},
                        "value": "3",
                    },
                    {
                        "text": {"type": "plain_text", "text": "4", "emoji": False},
                        "value": "4",
                    },
                    {
                        "text": {"type": "plain_text", "text": "5", "emoji": False},
                        "value": "5",
                    },
                ],
                "action_id": "edit_action_points",
                "initial_option": {
                    "text": {"type": "plain_text", "text": str(task.points), "emoji": False},
                    "value": str(task.points),
                }
            },
            "label": {"type": "plain_text", "text": "Points", "emoji": True},
        }
        block_actions_button = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Edit task"
            },
            "action_id": "edit_action_button",
            "value": str(task.task_id)
        }
        block_actions = {"type": "actions", "elements": []}
        block_actions["elements"].append(block_actions_button)

        blocks = []
        blocks.append(block_description)
        blocks.append(block_deadline)
        blocks.append(block_points)
        blocks.append(block_actions)
        blocks.append(block_tags)
        return blocks

    def is_editable(self):
        current_task_id = self.task_id
        helper = ErrorHelper()

        # check if task id exists
        exists = db.session.query(db.exists().where(Task.task_id == current_task_id)).scalar()

        task_progress = Assignment.query.filter_by(assignment_id=current_task_id, progress=0.0).all()

        if exists is False:
            return False, helper.get_command_help("no_task_id")

            # check if task is done
        elif exists is True and len(task_progress) == 0:
            return False, helper.get_command_help("cannot_edit_completed_task")

        # if task is not done
        elif exists is True and task_progress[0].progress == 0.0:
            return True, None

    def edit_task(self, desc, points, deadline, tags):
        """
        Edits a task in database and returns payload with success message

        :param desc: Description of task
        :type desc: str
        :param points: Points of task
        :type points: int
        :param deadline: Deadline of task
        :type deadline: Date
        :param deadline: ID of task
        :type deadline: int
        :raise:
        :return: Blocks list of response payload
        :rtype: list

        """
        db.session.query(Task).filter_by(task_id=self.task_id).update(
            dict(description=desc, points=points, deadline=deadline, tags = tags)
        )
        db.session.commit()
        response = deepcopy(self.base_edit_task_block_format)
        response["text"]["text"] = response["text"]["text"].format(greeting=random.choice(self.greetings), id=self.task_id)
        self.payload["blocks"].append(response)
        return self.payload["blocks"]

    def get_task(self):
        task = db.session.query(Task).filter_by(task_id=self.task_id).first()
        return task
