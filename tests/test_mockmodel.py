from models import Task, Assignment
from tests.mockmodels import mock_my_model, mock_get_sqlalchemy


def test_sqlalchemy_query_property_get_mock(
    mock_my_model,
    mock_get_sqlalchemy,
):
    """
    Test the view pending command

    :param mock_my_model: Mocked Task object
    :type mock_my_model: Task
    :param mock_get_sqlalchemy: Mocked SQL Alchemy object
    :type mock_get_sqlalchemy: Any
    :raise:
    :return: Assert if test case executed successfully
    :rtype: bool

    """
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_my_model
    ]
    response = (
        Task.query.join(Assignment)
        .add_columns(
            Assignment.progress,
            Task.task_id,
            Task.points,
            Task.description,
            Task.deadline,
        )
        .filter(Assignment.progress == 1.0)
        .all()
    )

    assert response == [mock_my_model]
