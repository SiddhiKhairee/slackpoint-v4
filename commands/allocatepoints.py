from models import Player, User, db
from helpers.errorhelper import ErrorHelper
from copy import deepcopy


class AllocatePoints:
    """
    This class handles all functionality related to the point reallocation of player characters.
    """

    base_allocate_points_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">You have come to understand a new power...\n\n"
                    ">*Character Class*: {prevClass} -> {newClass}\n\n"
                    ">*STR*: {prevSTR} -> {newSTR} ({diffSTR})\n"
                    ">*MAG*: {prevMAG} -> {newMAG} ({diffMAG})\n"
                    ">*DEF*: {prevDEF} -> {newDEF} ({diffDEF})\n"
                    ">*RES*: {prevRES} -> {newRES} ({diffRES})\n"
                    ">*AGL*: {prevAGL} -> {newAGL} ({diffAGL})\n"
                    ">*LUK*: {prevLUK} -> {newLUK} ({diffLUK})\n",
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

    def allocate_points_input_blocks(self):
        """
        Create blocks list containing input fields for class selection, all of the player stats, and
        a button to update the player character.

        :param:
        :type:
        :raise:
        :return: Blocks list
        :rtype: list

        """

        current_player = db.session.query(Player).filter_by(player_id=self.p_id).one()

        block_class_descriptor = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_quote",
                    "elements": [
                        {
                            "type": "text",
                            "text": "Change your class below if you'd like to. This will change your move set in battle."
                        }
                    ]
                }
            ]
        }
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
                "action_id": "allocate_points_class",
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
                            "text": "Set your stats down below. You can allocate your new points to your stats or rearrange"
                                    "your stats and class as long as the total is equal to your total stats.\n\n"
                                    "You have {} points to allocate.".format(getattr(current_player, "stat_points_to_allocate"))
                        }
                    ]
                }
            ]
        }
        block_strength = {
            "type": "input",
            "element": {
                "type": "number_input",
                "initial_value": str(getattr(current_player, "strength")),
                "min_value": "0",
                "max_value": "99",
                "is_decimal_allowed": False,
                "action_id": "allocate_points_strength",
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
                "initial_value": str(getattr(current_player, "magic")),
                "min_value": "0",
                "max_value": "99",
                "is_decimal_allowed": False,
                "action_id": "allocate_points_magic",
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
                "initial_value": str(getattr(current_player, "defense")),
                "min_value": "0",
                "max_value": "99",
                "is_decimal_allowed": False,
                "action_id": "allocate_points_defense",
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
                "initial_value": str(getattr(current_player, "resistance")),
                "min_value": "0",
                "max_value": "99",
                "is_decimal_allowed": False,
                "action_id": "allocate_points_resistance",
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
                "initial_value": str(getattr(current_player, "agility")),
                "min_value": "0",
                "max_value": "99",
                "is_decimal_allowed": False,
                "action_id": "allocate_points_agility",
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
                "initial_value": str(getattr(current_player, "luck")),
                "min_value": "0",
                "max_value": "99",
                "is_decimal_allowed": False,
                "action_id": "allocate_points_luck",
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
                "text": "Update Player"
            },
            "action_id": "allocate_points_button",
        }
        block_actions = {"type": "actions", "elements": []}
        block_actions["elements"].append(block_actions_button)

        blocks = []
        blocks.append(block_class_descriptor)
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

    def can_allocate_points(self) -> tuple[bool, str]:
        """
        Determines if the user already has a character created. If so, then return true. If not,
        return false and an error message.

        :return: A tuple containing whether the character can be updated and an error message if necessary
        :rtype: tuple[bool, str]
        """

        current_slack_user_id = self.slack_user_id
        helper = ErrorHelper()

        # Find if player_id exists in User
        current_user = db.session.query(User).filter_by(slack_user_id=current_slack_user_id).one()
        self.p_id = getattr(current_user, "player_id")
        player_existent = self.p_id is not None

        if player_existent:
            return True, None
        else:
            return False, helper.get_command_help("player_does_not_exist")

    def get_stat_total(self) -> int:
        """
        Finds the player from the database, and returns the current stat total and points that they are able to
        allocate.

        :return: The sum of all player stats and the points left for allocation
        :rtype: int
        """

        # Find if player_id exists in User
        current_slack_user_id = self.slack_user_id
        current_user = db.session.query(User).filter_by(slack_user_id=current_slack_user_id).one()
        p_id = getattr(current_user, "player_id")

        # Get player and get all statistical attributes
        current_player = db.session.query(Player).filter_by(player_id=p_id).one()
        p_str = int(getattr(current_player, "strength"))
        p_mag = int(getattr(current_player, "magic"))
        p_def = int(getattr(current_player, "defense"))
        p_res = int(getattr(current_player, "resistance"))
        p_agl = int(getattr(current_player, "agility"))
        p_luk = int(getattr(current_player, "luck"))
        p_pta = int(getattr(current_player, "stat_points_to_allocate"))

        # Return the sum of all the stats and the points still left to allocate
        return p_str + p_mag + p_def + p_res + p_agl + p_luk + p_pta

    def allocate_points(self, character_class: str, strength: int, magic: int, defense: int, resistance: int,
                        agility: int, luck: int) -> list:
        """
        Gets the character from the database and updates all stats and class fields. Returns a payload containinf success information.

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

        # Find if player_id exists in User
        current_slack_user_id = self.slack_user_id
        current_user = db.session.query(User).filter_by(slack_user_id=current_slack_user_id).one()
        p_id = getattr(current_user, "player_id")

        # Get player and get all statistical attributes
        current_player = db.session.query(Player).filter_by(player_id=p_id).one()

        # Stats before being updated
        p_class = getattr(current_player, "character_class")
        p_str = int(getattr(current_player, "strength"))
        p_mag = int(getattr(current_player, "magic"))
        p_def = int(getattr(current_player, "defense"))
        p_res = int(getattr(current_player, "resistance"))
        p_agl = int(getattr(current_player, "agility"))
        p_luk = int(getattr(current_player, "luck"))

        total_stat_pool = p_str + p_mag + p_def + p_res + p_agl + p_luk + getattr(current_player, "stat_points_to_allocate")

        # Query the User that the player should be assigned to and update the information
        db.session.query(Player).filter_by(player_id=p_id).update(
            dict(
                max_hp=300 + (20 * defense),
                max_mp=100 + (10 * magic),
                character_class=character_class,
                strength=strength,
                magic=magic,
                defense=defense,
                resistance=resistance,
                agility=agility,
                luck=luck,
                stat_points_to_allocate=total_stat_pool - strength - magic - defense - resistance - agility - luck
            )
        )
        db.session.commit()

        response = deepcopy(self.base_allocate_points_block_format)
        response["text"]["text"] = response["text"]["text"].format(
            prevClass=p_class, newClass=character_class,
            prevSTR=p_str, newSTR=strength, diffSTR=strength - p_str,
            prevMAG=p_mag, newMAG=magic, diffMAG=magic - p_mag,
            prevDEF=p_def, newDEF=defense, diffDEF=defense - p_def,
            prevRES=p_res, newRES=resistance, diffRES=resistance - p_res,
            prevAGL=p_agl, newAGL=agility, diffAGL=agility - p_agl,
            prevLUK=p_luk, newLUK=luck, diffLUK=luck - p_luk,
        )
        self.payload["blocks"].append(response)
        return self.payload["blocks"]
