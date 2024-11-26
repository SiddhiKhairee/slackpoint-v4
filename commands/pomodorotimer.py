import time
import threading
from datetime import datetime, timedelta
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from configuration.env_config import Config


class PomodoroTimer:
    """
    This class implements a Pomodoro Timer within the Slack bot.
    """
    
    
    def __init__(self, app):
        """
        Constructor to initialize the payload object for the Pomodoro Timer.

        :param:
        :type:
        :raise:
        :return: None
        :rtype: None
        """
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }
        self.app = app

    def timer_input_block(self):
        """
        Creates a block to input the total focus duration.

        :param:
        :type:
        :raise:
        :return: List of blocks
        :rtype: list
        """
        base_tell_user_their_time_started_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">Focus for the next 25 minutes!",
        },
    }

        block_timer_input = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "pomodoro_timer_duration",
                "placeholder": {"type": "plain_text", "text": "Enter duration in minutes"},
            },
            "label": {"type": "plain_text", "text": "Focus Duration", "emoji": True},
        }
        block_actions_button = {
            "type": "button",
            "text": {"type": "plain_text", "text": "Start Timer"},
            "action_id": "pomodoro_timer_start",
        }
        block_actions = {"type": "actions", "elements": [block_actions_button]}

        return [block_timer_input, block_actions]

    def start_pomodoro_timer(self, user_id, channel_id, total_minutes):
        """
        Starts the Pomodoro timer for a user with the specified total duration.

        :param user_id: Slack user ID
        :type user_id: str
        :param total_minutes: Total focus time in minutes
        :type total_minutes: int
        :raise:
        :return: None
        :rtype: None
        """
        slack_client = WebClient(Config.SLACK_BOT_TOKEN)
        slack_events_adapter = SlackEventAdapter(Config.SLACK_SIGNING_SECRET, "/slack/events", self.app)
        total_seconds = total_minutes * 60
        elapsed_time = 0

        def send_message_to_user(user_id, text):
            """
            Sends a message to the user in Slack.
            """
            # Here you'd implement the actual Slack API call to send a message
            
            print_blocks = [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"{text}",
                            },
                        }
                    ]
            slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=print_blocks
                    )

        def pomodoro_cycle():
            nonlocal elapsed_time
            while elapsed_time < total_seconds:
                # Work period
                send_message_to_user(user_id, "Focus for the next 25 minutes!")
                work_duration = min(1 * 60, total_seconds - elapsed_time) ###### changed from 25 to 1
                time.sleep(work_duration)
                elapsed_time += work_duration

                if elapsed_time >= total_seconds:
                    break

                # Break period
                send_message_to_user(user_id, "Your 5-minute break has started!")
                break_duration = min(0.5 * 60, total_seconds - elapsed_time) #### 5 to 0.5
                time.sleep(break_duration)
                elapsed_time += break_duration

            send_message_to_user(user_id, "Your Pomodoro session is complete! Great work!")

        # Running the Pomodoro timer in a separate thread to avoid blocking
        timer_thread = threading.Thread(target=pomodoro_cycle)
        timer_thread.start()

    def handle_action(self, action_id, user_id, value=None):
        """
        Handles the Slack interaction for starting the Pomodoro timer.

        :param action_id: ID of the Slack action triggered
        :type action_id: str
        :param user_id: Slack user ID
        :type user_id: str
        :param value: Value entered by the user (if applicable)
        :type value: str
        :raise:
        :return: None
        :rtype: None
        """
        if action_id == "pomodoro_timer_start":
            try:
                total_minutes = int(value)
                self.start_pomodoro_timer(user_id, total_minutes)
                return [{"type": "section", "text": {"type": "mrkdwn", "text": f"Pomodoro timer started for {total_minutes} minutes!"}}]
            except ValueError:
                return [{"type": "section", "text": {"type": "mrkdwn", "text": "Invalid input. Please enter a number for the duration."}}]
