from flask import jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from models import db, User, Player, Battle
from helpers.player_helper import get_player_by_slack_id
from helpers.battle_interactions import create_battle, get_battle_by_player
import re
from helpers.battlehelper import BattleHelper
from game.character_class_manager import CharacterClassManager
import os

slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
class_manager = CharacterClassManager()


def parse_opponent_id(text):
    match = re.search(r"<@([A-Z0-9]+)>", text)
    if match:
        return match.group(1)
    return None


def handle_battle_command(user_id, text):
    # Parse the opponent's Slack ID from the text
    opponent_slack_id = parse_opponent_id(text)
    if not opponent_slack_id:
        return jsonify(
            response_type="ephemeral",
            text="Please specify an opponent using their Slack ID.",
        )

    # Get player objects
    player1 = get_player_by_slack_id(user_id)
    player2 = get_player_by_slack_id(opponent_slack_id)

    if not player1 or not player2:
        return jsonify(
            response_type="ephemeral",
            text="Both players must have a character. Use `/create-character` to create one.",
        )

    # Check if a battle already exists for player1
    existing_battle = get_battle_by_player(player1.player_id)
    if existing_battle:
        return jsonify(response_type="ephemeral", text="You are already in a battle.")

    # Check if player2 is already in a battle
    existing_battle_opponent = get_battle_by_player(player2.player_id)
    if existing_battle_opponent:
        return jsonify(
            response_type="ephemeral", text="Your opponent is already in a battle."
        )

    # Create a new battle
    battle = create_battle(player1.player_id, player2.player_id)

    # Notify both players
    return jsonify(
        response_type="in_channel",
        text=f"<@{user_id}> has challenged <@{opponent_slack_id}> to a battle!",
    )


def handle_attack_command(user_id, channel_id):
    # 1. Retrieve the player and battle
    player = get_player_by_slack_id(user_id)
    if not player:
        return jsonify(
            response_type="ephemeral", text="You need to create a character first."
        )

    battle = get_battle_by_player(player.player_id)
    if not battle:
        return jsonify(
            response_type="ephemeral", text="You are not currently in a battle."
        )

    # 2. Verify it's the player's turn
    if battle.current_turn_player_id != player.player_id:
        return jsonify(response_type="ephemeral", text="It is not your turn.")

    # 3. Get the opponent
    opponent = (
        battle.player2 if battle.player_id_1 == player.player_id else battle.player1
    )
    if not opponent:
        return jsonify(response_type="ephemeral", text="Opponent not found.")

    # 4. Retrieve current stats
    player_hp = battle.get_hp_remaining(player.player_id)
    player_mp = battle.get_mp_remaining(player.player_id)
    opponent_hp = battle.get_hp_remaining(opponent.player_id)

    # 5. Get the player's move set
    move_list = class_manager.move_dict.get(player.character_class)
    if not move_list:
        return jsonify(response_type="ephemeral", text="You have no moves available.")

    # 6. Build the interactive message blocks
    blocks = build_attack_message_blocks(battle, player, opponent, move_list)

    # 7. Send the message to the player
    try:
        slack_client.chat_postMessage(
            channel=channel_id, blocks=blocks, text="Your turn!"
        )
    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")
        return jsonify(
            response_type="ephemeral",
            text="An error occurred while sending the message.",
        )

    return "", 200  # Acknowledge the command


def build_attack_message_blocks(battle, player, opponent, move_list):
    # Retrieve current stats
    player_hp = battle.get_hp_remaining(player.player_id)
    player_mp = battle.get_mp_remaining(player.player_id)
    opponent_hp = battle.get_hp_remaining(opponent.player_id)

    # Build move options for the dropdown
    options = []
    for index, move in enumerate(move_list):
        option = {
            "text": {
                "type": "plain_text",
                "text": f"{index + 1}) {move.name} ({move.base_power} power, {move.base_hit_rate}% hit) {move.mp_cost} MP",
            },
            "value": str(index),  # Use the index as the value
        }
        options.append(option)

    # Build the message blocks
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Opponent HP:* {opponent_hp}/{opponent.max_hp}\n"
                f"*Your HP:* {player_hp}/{player.max_hp}\n"
                f"*Your MP:* {player_mp}/{player.max_mp}\n"
                f"*Your turn!*",
            },
        },
        {"type": "divider"},
        {
            "type": "input",
            "block_id": "move_selection_block",
            "label": {"type": "plain_text", "text": "Select your move:"},
            "element": {
                "type": "static_select",
                "action_id": "move_selection",
                "placeholder": {"type": "plain_text", "text": "Choose a move"},
                "options": options,
            },
        },
    ]

    return blocks
