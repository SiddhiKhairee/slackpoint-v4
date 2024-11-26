from copy import deepcopy
import random
from models import *
from datetime import date

class ShowStore:
    """
    This class show the product in the store.
    """
    base_create_store_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Product Store*\n\n*Name* | *Price* | *Description*\n\n1. Large food | $3 | Restores 3 HP\n2. Medium food | $2 | Restores 2 HP\n3. Small food | $1 | Restores 1 HP"
        }
    }
    def __init__(self):
        """
        Constructor to initialize payload object

        :param:
        :type:
        :raise:
        :return: None
        :rtype: None

        """
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }
    
    def show_store(self):
        """
        Create blocks list containing input fields for name, price and description

        :param:
        :type:
        :raise:
        :return: Blocks list
        :rtype: list

        """
        

        self.payload["blocks"].append(deepcopy(self.base_create_store_block_format))
        return self.payload
    