from models import Player, User, db
from helpers.errorhelper import ErrorHelper
from copy import deepcopy


class CreateCharacter:
    """
    This class handles all functionality related to the creation of player characters.
    """

    base_allocate_points_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">Your character (ID: {id}, Class: {char_class}) allocated its points successfully.",
        },
    }

    def __init__(self, user_id):
        """
        Constructor to initialize payload object

        :param:
        :type:
        :raise:
        :return: None
        :rtype: None

        """

        self.user_id = user_id
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }

    def allocate_input_blocks(self):
        """
        Create blocks list containing input fields for description, deadline, points of a task, along with a button to create the task

        :param:
        :type:
        :raise:
        :return: Blocks list
        :rtype: list

        """

        block_strength = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_character_strength",
            },
            "label": {"type": "plain_text", "text": "Strength", "emoji": True},
        }
        block_magic = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_character_magic",
            },
            "label": {"type": "plain_text", "text": "Magic", "emoji": True},
        }
        block_defense = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_character_defense",
            },
            "label": {"type": "plain_text", "text": "Defense", "emoji": True},
        }
        block_resistance = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_character_resistance",
            },
            "label": {"type": "plain_text", "text": "Resistance", "emoji": True},
        }
        block_agility = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_character_agility",
            },
            "label": {"type": "plain_text", "text": "Agility", "emoji": True},
        }
        block_luck = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_character_luck",
            },
            "label": {"type": "plain_text", "text": "Luck", "emoji": True},
        }
        block_actions_button = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Create Player"
            },
            "action_id": "create_character_button",
        }
        block_actions = {"type": "actions", "elements": []}
        block_actions["elements"].append(block_actions_button)

        blocks = []
        blocks.append(block_strength)
        blocks.append(block_magic)
        blocks.append(block_defense)
        blocks.append(block_resistance)
        blocks.append(block_agility)
        blocks.append(block_luck)
        blocks.append(block_actions)
        return blocks

    def can_allocate_points(self) -> tuple[bool, str]:
        """
        Determines if the user already has a character created. If so, then return false and an
        error message. If not, return true and a null error message, signifying success.

        :return: A tuple containing whether the character can be created and an error message if necessary
        :rtype: tuple[bool, str]
        """

        current_user_id = self.user_id
        helper = ErrorHelper()

        # Find if player_id exists in User
        player_existent = db.session.query(db.exists().where(User.user_id == current_user_id and User.player_id is not None)).scalar()

        # TODO: Check if the player actually has points to allocate

        if not player_existent:
            return True, None
        else:
            return False, helper.get_command_help("player_exists")

    def allocate_points(self, strength: int, magic: int, defense: int, resistance: int,
                         agility: int, luck: int) -> list:
        """
        Creates a character in the database and returns a payload with the success message along with the newly created player ID

        :param character_class: The character class for the player that defines the moves they can use
        :param strength: The strength value of the player for physical attacks
        :param magic: The magic value of the player for magic attacks
        :param defense: The defense value to protect against physical attacks
        :param resistance: The resistance value to protect against magic attacks
        :param agility: The agility value to increase hit rate and evasion, as well as influence turn order
        :param luck: The luck value that makes random damage output skew more in your favor
        :raise:
        :return: List of response payload blocks
        :rtype: list

        """

        # Database call to add a character and get a generated ID
        player = Player()
        player.strength = strength
        player.magic = magic
        player.defense = defense
        player.resistance = resistance
        player.agility = agility
        player.luck = luck
        player.stat_points_to_allocate = 0
        db.session.add(player)
        db.session.commit()
        db.session.refresh(player)

        # Get the ID of the player
        p_id = player.player_id

        # Query the User that the player should be assigned to and update the information
        db.session.query(User).filter_by(user_id=self.user_id)
        db.session.commit()

        response = deepcopy(self.base_create_character_block_format)
        response["text"]["text"] = response["text"]["text"].format(char_class=character_class, id=id)
        self.payload["blocks"].append(response)
        return self.payload["blocks"]
