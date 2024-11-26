from copy import deepcopy
import random
from models import *
from datetime import date
import helpers.user_helper as uh
from flask import request

class ShowInventory:
    """
    This class show the product in the inventory.
    """
    base_showinventory_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "{position}. {ProductName} | {Quantity} | {Description} \n"
			
        }
    }
    def __init__(self):
       self.payload = {"response_type": "ephemeral", "blocks": []}

    def add_default_inventory(self, userID):
        # Check if the inventory table is empty
        if db.session.query(Inventory).count() == 0:
            user = uh.check_user_exists(userID)
            # Add default inventory
            inventory1 = Inventory(product_id=1, user_id=user.user_id, quantity=0)
            inventory2 = Inventory(product_id=2, user_id=user.user_id, quantity=0)
            inventory3 = Inventory(product_id=3, user_id=user.user_id, quantity=0)
            db.session.add(inventory1)
            db.session.add(inventory2)
            db.session.add(inventory3)
            db.session.commit()

    def get_inventory(self, slack_user_id):
        """
        Create blocks list containing input fields for name, price and description
        """
        user = uh.check_user_exists(slack_user_id)

        get_inventory = (
            db.session.query(
                Inventory.inventory_id,
                Product.name,
                Product.price,
                Product.description,
                Inventory.quantity
            )
            .join(Product, Inventory.product_id == Product.product_id)  # Join Inventory with Product
            .join(User, Inventory.user_id == User.user_id)              # Join Inventory with User
            .filter(User.user_id == user.user_id)                                  # Filter by specific user ID
            .all()
        )

        block_title = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": " *Your Inventory*\n\n*Product* | *Quantity* | *Description*\n"
            }
        }
        self.payload["blocks"].append(block_title)
        count =0
        for product in get_inventory:
            count+=1
            response_payload = deepcopy(self.base_showinventory_block_format)
            response_payload["text"]["text"] = response_payload["text"]["text"].format(
                position = count, ProductName=product.name, Quantity=product.quantity, Description=product.description
            )
            self.payload["blocks"].append(response_payload)

        return self.payload