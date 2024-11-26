from commands.viewpoints import ViewPoints
from configuration.env_config import Config
from commands.createtask import CreateTask
from commands.taskdone import TaskDone
from commands.leaderboard import Leaderboard
from mock import patch
from commands.summary import Summary
from tests.mockmodels import (
    mock_pending_task_1,
    mock_pending_task_2,
    mock_get_sqlalchemy,
    mock_leaderboard_position_1,
    mock_leaderboard_position_2,
)


@patch.object(Leaderboard, "view_leaderboard")
def test_get_summary(
    mocker,
    mock_pending_task_1,
    mock_pending_task_2,
    mock_get_sqlalchemy,
    mock_leaderboard_position_1,
    mock_leaderboard_position_2,
):
    mocker.return_value = {"blocks": [{"text": {"text": "pbrr"}}]}
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_pending_task_1,
        mock_pending_task_2,
    ]
    Summary().get_summary()
