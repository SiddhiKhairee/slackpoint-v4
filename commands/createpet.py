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

    base_no_pet_food_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "You don't have any pet food! Use the `/showstore` command to buy some."
        }
    }

    base_only_1_pet_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "You can only have one pet at a time. Use the `/pet-status` command to check your pet's status."
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

    def create_pet_input_blocks(self, slack_user_id):
        user = uh.check_user_exists(slack_user_id)
        pet = db.session.query(Pet).filter_by(user_id=user.user_id).first()
        if pet is not None:
            return [self.base_only_1_pet_block_format]
        
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
    
    def feed_pet_input_blocks(self, slack_user_id):
        user = uh.check_user_exists(slack_user_id)
        # Query inventory options of user_id and show if quantity > 0
        inventory_options = db.session.query(Inventory).filter_by(user_id=user.user_id).filter(Inventory.quantity > 0).all()
        if len(inventory_options) == 0:
            return [self.base_no_pet_food_block_format]
        block_inventory_drop_down = {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item to feed your pet"
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": f"{db.session.query(Product).filter_by(product_id=inventory.product_id).first().name} - Quantity available: {inventory.quantity}"
                        },
                        "value": str(inventory.inventory_id)  # Assuming inventory.id is the primary key
                    }
                    for inventory in inventory_options  # Loop through each inventory object
                ],
                "action_id": "feed_pet_inventory_select",
            },
            "label": {
                "type": "plain_text",
                "text": "Inventory",
                "emoji": True
            }
        }
        block_feed_pet_button = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Feed Pet"},
                    "style": "primary",
                    "value": "feed_pet",
                    "action_id": "feed_pet_action_button"
                }
            ]
        }

        blocks = []
        blocks.append(block_inventory_drop_down)
        blocks.append(block_feed_pet_button)

        return blocks

    def feed_pet(self, slack_user_id, inventory_id):
        user = uh.check_user_exists(slack_user_id)
        pet = db.session.query(Pet).filter_by(user_id=user.user_id).first()
        inventory = db.session.query(Inventory).filter_by(inventory_id=inventory_id).first()
        product = db.session.query(Product).filter_by(product_id=inventory.product_id).first()

        if pet is None:
            return [self.base_no_pet_block_format]
        
        if inventory.quantity - 1 < 0:
            return [self.base_no_pet_food_block_format]
        
        # decrement from inventory
        db.session.query(Inventory).filter_by(inventory_id=inventory_id).update({"quantity": inventory.quantity - 1})
        db.session.commit()

        # update pet hp
        db.session.query(Pet).filter_by(id=pet.id).update({"hp": pet.hp + product.price})
        db.session.commit()

        return [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{pet.pet_name} was fed {product.name} and gained {product.price} HP! Your pet now has {pet.hp} HP."
            }
        }]