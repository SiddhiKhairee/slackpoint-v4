from commands.viewpoints import ViewPoints
from configuration.env_config import Config
from commands.createtask import CreateTask
from commands.taskdone import TaskDone
from commands.leaderboard import Leaderboard


class Summary:
    def __init__(self):
        pass

    def get_summary(self):
        vp = ViewPoints(progress=0.0)
        payload = vp.get_list()
        pending_tasks = ""
        for task in payload:
            taskid = task[0]
            points = task[3]
            taskname = task[4]
            taskdate = task[5]

            pending_tasks += """ Task ID: {taskid} ({pts} SlackPoints) {taskname} [Deadline: {dt}]./n""".format(
                taskid=taskid, pts=points, taskname=taskname, dt=taskdate
            )

        # leaderboard display
        payload = Leaderboard().view_leaderboard()

        leaderboard_msg = ""
        for block in payload["blocks"]:
            leaderboard_msg += str(block["text"]["text"]) + "/n"

        # completed Tasks
        vp = ViewPoints(progress=1.0)
        payload = vp.get_list()

        completed_tasks = ""

        messages = [
            "Summary is : ",
        ]

        parent_msg = {"blocks": []}
        child_msg = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*Summary is :*"},
        }
        parent_msg["blocks"].append(child_msg)
        child_msg = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Pending Tasks are:"},
        }
        parent_msg["blocks"].append(child_msg)

        vp = ViewPoints(progress=0.0)
        payload = vp.get_list()
        for task in payload["blocks"]:
            child_msg = {
                "type": "section",
                "text": {"type": "mrkdwn", "text": task["text"]["text"]},
            }
            parent_msg["blocks"].append(child_msg)
        # completed tasks
        child_msg = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Completed Tasks are:"},
        }
        parent_msg["blocks"].append(child_msg)
        vp = ViewPoints(progress=1.0)
        payload = vp.get_list()
        for task in payload["blocks"]:
            child_msg = {
                "type": "section",
                "text": {"type": "mrkdwn", "text": task["text"]["text"]},
            }
            parent_msg["blocks"].append(child_msg)
            # Leaderboard
            child_msg = {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "Leaderboard Status:"},
            }
            parent_msg["blocks"].append(child_msg)
            payload = Leaderboard().view_leaderboard()
            for task in payload["blocks"]:
                child_msg = {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": task["text"]["text"]},
                }
                parent_msg["blocks"].append(child_msg)

            return parent_msg
