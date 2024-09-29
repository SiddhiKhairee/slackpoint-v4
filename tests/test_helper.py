import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from helpers import helper
from mock import patch
import os
import pytest

@patch.object(WebClient, '__init__')
def test_send_slack_message(mock_client):
    mock_client.return_value = None
    mock_client.chat_postMessage.return_value = True
    os.environ['SLACK_BOT_TOKEN'] = "token"
    with pytest.raises(Exception) as e_info:
        helper.send_slack_message({"blocks": "hola"})

