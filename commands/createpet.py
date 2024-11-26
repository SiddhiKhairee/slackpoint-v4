from copy import deepcopy
from models import *
from datetime import date
import helpers.user_helper as uh

class CreatePet:
    """
    This class handles the Create Pet functionality.
    """

    base_create_pet_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Thats a cute name! Your pet {pet_name} was created successfully.",
        },
    }

    base_no_pet_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "You don't have a pet yet! Use the `/create-pet` command to create one."
        }
    }

    default_pet_starting_hp = 5

    def __init__(self):
        """
        Constructor to initialize payload object

        :param:
        :type:
        :raise:
        :return: None
        """
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }

    def create_pet_input_blocks(self):
        block_pet_name_input = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_action_pet_name",
            },
            "label": {"type": "plain_text", "text": "Pet Name", "emoji": True},
        }
        block_create_pet_button = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Create Pet"},
                    "style": "primary",
                    "value": "create_pet",
                    "action_id": "create_pet_action_button"
                }
            ]
        }

        blocks = []
        blocks.append(block_pet_name_input)
        blocks.append(block_create_pet_button)

        return blocks

    def create_pet(self, slack_user_id, pet_name):
        """
        Create a pet for the user

        :param slack_user_id: The slack user's ID
        :type user_id: str
        :param pet_name: The name of the pet
        :type pet_name: str
        :return: The pet that was created
        :rtype: Pet
        """
        user = uh.check_user_exists(slack_user_id)
        

        pet = Pet(user_id=user.user_id, pet_name=pet_name, hp=self.default_pet_starting_hp)
        db.session.add(pet)
        db.session.commit()
        
        response = deepcopy(self.base_create_pet_block_format)
        response["text"]["text"] = response["text"]["text"].format(pet_name=pet_name)
        self.payload["blocks"].append(response)
        return self.payload["blocks"]
    
    def show_pet_status(self, slack_user_id):
        """
        Show the status of the pet

        :param slack_user_id: The slack user's ID
        :type user_id: str
        :return: The pet status
        :rtype: Pet
        """
        user = uh.check_user_exists(slack_user_id)

        pet = db.session.query(Pet).filter_by(user_id=user.user_id).first()
        if pet is None:
            return [].append(self.base_no_pet_block_format)

        blocks = []
        block_pet_status = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{pet.pet_name}*\nHP: {pet.hp}\n{pet.hp < 3 and 'Your pet is weak & hungry! Feed it!' or ''}"
            }
        }
        blocks.append(block_pet_status)
        return blocks