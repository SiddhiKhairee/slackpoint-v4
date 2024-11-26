import time

class PomodoroTimer:
    '''This class will implement a simple pomodoro timer'''
    block_duration = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_action_description",
            },
            "label": {"type": "plain_text", "text": "Description", "emoji": True},
        }