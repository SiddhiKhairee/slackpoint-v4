from models import Player, User, db
from helpers.errorhelper import ErrorHelper
from copy import deepcopy


class CreateCharacter:
    """
    This class handles all functionality related to the creation of player characters.
    """

    base_create_character_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">Your character (Class: {char_class}) was created successfully.",
        },
    }

    def __init__(self, slack_user_id: str):
        """
        Constructor to initialize payload object

        :param:
        :type:
        :raise:
        :return: None
        :rtype: None

        """

        self.slack_user_id = slack_user_id
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }

    def create_character_input_blocks(self):
        """
        Create blocks list containing input fields for class selection, all of the player stats, and
        a button to create the player character.

        :param:
        :type:
        :raise:
        :return: Blocks list
        :rtype: list

        """

        block_class_selection = {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {"type": "plain_text", "text": "Select a class", "emoji": True},
                "options": [
                    {
                        "text": {"type": "plain_text", "text": "Swordmaster", "emoji": False},
                        "value": "Swordmaster",
                    },
                    {
                        "text": {"type": "plain_text", "text": "Fire Mage", "emoji": False},
                        "value": "Fire Mage",
                    }
                ],
                "action_id": "create_character_class",
            },
            "hint": {
                "type": "plain_text",
                "text": "Select a character class for yourself! This determines what moves you will be able to use in battle.",
                "emoji": True
            },
            "label": {"type": "plain_text", "text": "Character Class", "emoji": True},
        }
        block_stat_descriptor = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_quote",
                    "elements": [
                        {
                            "type": "text",
                            "text": "Set your stats down below. You can only start with a stat total of 20."
                        }
                    ]
                }
            ]
        }
        block_strength = {
            "type": "input",
            "element": {
                "type": "number_input",
                "initial_value": "0",
                "min_value": "0",
                "max_value": "20",
                "is_decimal_allowed": False,
                "action_id": "create_character_strength",
            },
            "hint": {
                "type": "plain_text",
                "text": "The amount of strength a character has represents the amount of physical strength it has",
                "emoji": True
            },
            "label": {"type": "plain_text", "text": "Strength", "emoji": True},
        }
        block_magic = {
            "type": "input",
            "element": {
                "type": "number_input",
                "initial_value": "0",
                "min_value": "0",
                "max_value": "20",
                "is_decimal_allowed": False,
                "action_id": "create_character_magic",
            },
            "hint": {
                "type": "plain_text",
                "text": "The amount of magic prowess a character has to use magic attacks",
                "emoji": True
            },
            "label": {"type": "plain_text", "text": "Magic", "emoji": True},
        }
        block_defense = {
            "type": "input",
            "element": {
                "type": "number_input",
                "initial_value": "0",
                "min_value": "0",
                "max_value": "20",
                "is_decimal_allowed": False,
                "action_id": "create_character_defense",
            },
            "hint": {
                "type": "plain_text",
                "text": "A value used to reduce the amount of damage done by physical attacks",
                "emoji": True
            },
            "label": {"type": "plain_text", "text": "Defense", "emoji": True},
        }
        block_resistance = {
            "type": "input",
            "element": {
                "type": "number_input",
                "initial_value": "0",
                "min_value": "0",
                "max_value": "20",
                "is_decimal_allowed": False,
                "action_id": "create_character_resistance",
            },
            "hint": {
                "type": "plain_text",
                "text": "A value used to reduce the amount of damage done by magical attacks",
                "emoji": True
            },
            "label": {"type": "plain_text", "text": "Resistance", "emoji": True},
        }
        block_agility = {
            "type": "input",
            "element": {
                "type": "number_input",
                "initial_value": "0",
                "min_value": "0",
                "max_value": "20",
                "is_decimal_allowed": False,
                "action_id": "create_character_agility",
            },
            "hint": {
                "type": "plain_text",
                "text": "A value used to determine the hit rate and dodge rate of the character. Whoever has more agility will get the first turn in battle.",
                "emoji": True
            },
            "label": {"type": "plain_text", "text": "Agility", "emoji": True},
        }
        block_luck = {
            "type": "input",
            "element": {
                "type": "number_input",
                "initial_value": "0",
                "min_value": "0",
                "max_value": "20",
                "is_decimal_allowed": False,
                "action_id": "create_character_luck",
            },
            "hint": {
                "type": "plain_text",
                "text": "A value used to slightly influence the chance to hit and dodge. It also factors into any RNG-based decisions that may occur during battle",
                "emoji": True
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
        blocks.append(block_class_selection)
        blocks.append(block_stat_descriptor)
        blocks.append(block_strength)
        blocks.append(block_magic)
        blocks.append(block_defense)
        blocks.append(block_resistance)
        blocks.append(block_agility)
        blocks.append(block_luck)
        blocks.append(block_actions)
        return blocks

    def can_create_character(self) -> tuple[bool, str]:
        """
        Determines if the user already has a character created. If so, then return false and an
        error message. If not, return true and a null error message, signifying success.

        :return: A tuple containing whether the character can be created and an error message if necessary
        :rtype: tuple[bool, str]
        """

        current_slack_user_id = self.slack_user_id
        helper = ErrorHelper()

        # Find if player_id exists in User
        current_user = db.session.query(User).filter_by(slack_user_id=current_slack_user_id).one()
        p_id = getattr(current_user, "player_id")
        player_existent = p_id is not None

        if not player_existent:
            return True, None
        else:
            return False, helper.get_command_help("player_exists")

    def create_character(self, character_class: str, strength: int, magic: int, defense: int, resistance: int,
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
        player.max_hp = 300 + (20 * defense)
        player.max_mp = 100 + (10 * magic)
        player.character_class = character_class
        player.strength = strength
        player.magic = magic
        player.defense = defense
        player.resistance = resistance
        player.agility = agility
        player.luck = luck
        # If the player has not allocated all 20 points, put them in reserve
        player.stat_points_to_allocate = 20 - strength - magic - defense - resistance - agility - luck
        db.session.add(player)
        db.session.commit()
        db.session.refresh(player)

        # Get the ID of the player
        p_id = player.player_id

        # Query the User that the player should be assigned to and update the information
        db.session.query(User).filter_by(slack_user_id=self.slack_user_id).update(
            dict(player_id=p_id)
        )
        db.session.commit()

        response = deepcopy(self.base_create_character_block_format)
        response["text"]["text"] = response["text"]["text"].format(char_class=character_class)
        self.payload["blocks"].append(response)
        return self.payload["blocks"]
