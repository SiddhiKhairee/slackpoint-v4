from copy import deepcopy
import random
from models import *
from datetime import date
import helpers.user_helper as uh

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

    base_no_money_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "You do not have enough points to buy this item. Go get some work done!"
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
        block_input_product_id_to_buy = {
            "type": "input",
            "element": {
                "type": "static_select",
                "action_id": "product_id_to_buy",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "1. Large food | $3 | Restores 3 HP"
                        },
                        "value": "1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "2. Medium food | $2 | Restores 2 HP"
                        },
                        "value": "2"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "3. Small food | $1 | Restores 1 HP"
                        },
                        "value": "3"
                    }
                ]
            },
            "label": {
                "type": "plain_text",
                "text": "Product ID to Buy"
            }
        }          
        block_buy_item_button = {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "Continue to buy the item by clicking the button here"
          },
          "accessory": {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Buy Item",
              "emoji": True
            },
            "action_id": "buy_action_button"
          }
        }
        blocks.append(response_payload)
        blocks.append(block_input_product_id_to_buy)
        blocks.append(block_buy_item_button)

        return blocks

    def buy_item(self, slack_user_id, product_id):
        """
        Buy the product from the store, updates your inventory and reduces your points earned
        """

        user = uh.check_user_exists(slack_user_id)
        product = db.session.query(Product).filter_by(product_id=product_id).first()
        
        # Check if user has enough points to buy the product
        if (user.points_earned - product.price) < 0:
            self.payload["blocks"].append(self.base_no_money_block_format)
            return self.payload["blocks"]

        # Reduce earned points by the price of the product in user table
        user.points_earned -= product.price

        # Update user inventory with the product bought
        user_inventory = db.session.query(Inventory).filter_by(user_id=user.user_id, product_id=product.product_id).first()
        if user_inventory is None:
            user_inventory = Inventory(user_id=user.user_id, product_id=product.product_id, quantity=1)
            db.session.add(user_inventory)
        else:
            db.session.query(Inventory).filter_by(user_id=user.user_id, product_id=product.product_id).update({"quantity": user_inventory.quantity + 1})
        db.session.commit()
        

        self.payload["blocks"].append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Successfully bought {product.name}. You now have {user.points_earned} points left."
            }
        })
        return self.payload["blocks"]