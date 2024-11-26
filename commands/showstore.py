from copy import deepcopy
import random
from models import *
from datetime import date

class ShowStore:
    """
    This class show the product in the store.
    """
    base_showstore_block_format = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Product Store*\n\n*Name* | *Price* | *Description*\n\n1. Large food | $3 | Restores 3 HP\n2. Medium food | $2 | Restores 2 HP\n3. Small food | $1 | Restores 1 HP"
			}
		}
    def __init__(self):
       self.payload = {"response_type": "ephemeral", "blocks": []}

    def create_show_store_blocks(self):
        """
        Create blocks list containing input fields for name, price and description
        """
        blocks = []
        response_payload = deepcopy(self.base_showstore_block_format)
        blocks.append(response_payload)

        return blocks
    