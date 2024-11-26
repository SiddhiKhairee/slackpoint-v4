from commands.createpet import CreatePet
from unittest.mock import MagicMock, patch
import pytest


def test_create_pet_input_blocks():

    # test function
    cp = CreatePet()
    payload = cp.create_pet_input_blocks()

    # expectation
    expected_payload = [{'type': 'input', 'element': {'type': 'plain_text_input', 'action_id': 'create_action_pet_name'}, 'label': {'type': 'plain_text', 'text': 'Pet Name', 'emoji': True}}, {'type': 'actions', 'elements': [{'type': 'button', 'text': {'type': 'plain_text', 'text': 'Create Pet'}, 'style': 'primary', 'value': 'create_pet', 'action_id': 'create_pet_action_button'}]}]
    print(payload)

    # assertion
    assert payload == expected_payload
    
@patch('models.db.session')
@patch('models.User')
@patch('models.Pet')
def test_create_pet(mock_pet, mock_user, mock_db_session):
    # Mock the user query
    mock_user_query = mock_db_session.query.return_value.filter_by.return_value
    mock_user_query.first.return_value = None  # Simulate user not found
    
    # Mock creating a new user
    mock_user_instance = mock_user.return_value
    mock_user_instance.user_id = 1  # Mock user_id for the new user
    
    # Mock the Pet model
    mock_pet_instance = mock_pet.return_value
    
    # Mock the CreatePet instance
    cp = CreatePet()
    cp.default_pet_starting_hp = 100  # Set a mock value for starting HP
    cp.base_create_pet_block_format = {"text": {"text": "Created pet: {pet_name}"}}
    cp.payload = {"blocks": []}

    # Call the function
    payload = cp.create_pet(pet_name="TestPet", slack_user_id="ABC123")

    # Assertions
    mock_db_session.add.assert_called()  # Ensure db session's add was called
    mock_db_session.commit.assert_called()  # Ensure db commit was called
    assert payload[-1]["text"]["text"] == "Created pet: TestPet"
    assert len(payload) == 1

@patch('models.db.session')
@patch('models.User')
@patch('models.Pet')
def test_show_pet_status_with_pet(mock_pet, mock_user, mock_db_session):
    # Mock user query
    mock_user_query = mock_db_session.query.return_value.filter_by.return_value
    mock_user_instance = mock_user.return_value
    mock_user_query.first.return_value = mock_user_instance
    mock_user_instance.user_id = 1

    # Mock pet query
    mock_pet_query = mock_db_session.query.return_value.filter_by.return_value
    mock_pet_instance = mock_pet.return_value
    mock_pet_instance.pet_name = "Fluffy"
    mock_pet_instance.hp = 5
    mock_pet_query.first.return_value = mock_pet_instance

    # Mock CreatePet instance
    cp = CreatePet()
    cp.base_no_pet_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "You don't have a pet yet! Use the `/create-pet` command to create one."
        }
    }

    # Call the function
    result = cp.show_pet_status(slack_user_id="ABC123")

    # Assertions
    assert len(result) == 1
    assert result[0]["text"]["text"] == "*Fluffy*\nHP: 5\n"

@patch('models.db.session')
@patch('models.User')
@patch('models.Pet')
def test_show_pet_status_no_pet(mock_pet, mock_user, mock_db_session):
    # Mock user query
    mock_user_query = mock_db_session.query.return_value.filter_by.return_value
    mock_user_instance = mock_user.return_value
    mock_user_query.first.return_value = mock_user_instance
    mock_user_instance.user_id = 1

    # Mock pet query (returns None)
    mock_pet_query = mock_db_session.query.return_value.filter_by.return_value
    mock_pet_query.first.return_value = None

    # Mock CreatePet instance
    cp = CreatePet()
    cp.base_no_pet_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "You don't have a pet yet! Use the `/create-pet` command to create one."
        }
    }

    # Call the function
    cp.show_pet_status(slack_user_id="ABC123")
