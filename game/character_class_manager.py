import json
from move import Move


class CharacterClassManager:
    """
    Initializes the CharacterClassManager and populates the move dictionary with each class
    and their respective movelists.

    :cvar move_dict: A dictionary containing a movelist for each class
    """

    def __init__(self):
        """
        Initializes the CharacterClassManager and populates the move dictionary with each class
        and their respective movelists.
        """

        # Load in the characterclasses.json file
        json_loader = json.load(open("game/characterclasses.json", "r"))

        # Populate the dictionary with each class and their movelists
        self.move_dict = {}
        # Populate the dictionary with each class and their movelists
        for class_name in json_loader:
            # Create empty move list for class, then populate it with moves
            move_list = []
            for move_json in json_loader[class_name]:
                move = Move(**move_json)
                move_list.append(move)
            # Add the movelist to the dictionary
            self.move_dict[class_name] = move_list
