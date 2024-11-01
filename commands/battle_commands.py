from flask import jsonify
from helpers.player_helper import get_player_by_slack_id
from helpers.battle_interactions import create_battle, get_battle_by_player
import re

def parse_opponent_id(text):
    match = re.search(r'<@([A-Z0-9]+)>', text)
    if match:
        return match.group(1)
    return None

def handle_battle_command(user_id, text):
    # Parse the opponent's Slack ID from the text
    opponent_slack_id = parse_opponent_id(text)
    if not opponent_slack_id:
        return jsonify(response_type='ephemeral', text='Please specify an opponent using their Slack ID.')

    # Get player objects
    player1 = get_player_by_slack_id(user_id)
    player2 = get_player_by_slack_id(opponent_slack_id)

    if not player1 or not player2:
        return jsonify(response_type='ephemeral', text='Both players must have a character. Use `/create-character` to create one.')

    # Check if a battle already exists for player1
    existing_battle = get_battle_by_player(player1.player_id)
    if existing_battle:
        return jsonify(response_type='ephemeral', text='You are already in a battle.')

    # Check if player2 is already in a battle
    existing_battle_opponent = get_battle_by_player(player2.player_id)
    if existing_battle_opponent:
        return jsonify(response_type='ephemeral', text='Your opponent is already in a battle.')

    # Create a new battle
    battle = create_battle(player1.player_id, player2.player_id)

    # Notify both players
    return jsonify(response_type='in_channel', text=f'<@{user_id}> has challenged <@{opponent_slack_id}> to a battle!')


def handle_attack_command(user_id):
    # Retrieve player's battle
    player = get_player_by_slack_id(user_id)
    battle = get_battle_by_player(player.player_id)
    if not battle:
        return jsonify(response_type='ephemeral', text='You are not in a battle.')

    # Determine opponent
    if battle.player_id_1 == player.player_id:
        opponent_player_id = battle.player_id_2
        opponent_hp = battle.hp_remaining_2
        opponent = battle.player2
        attacker_hp = battle.hp_remaining_1
    else:
        opponent_player_id = battle.player_id_1
        opponent_hp = battle.hp_remaining_1
        opponent = battle.player1
        attacker_hp = battle.hp_remaining_2

    # Calculate damage
    damage = BattleHelper.calculate_damage(
        user_atk=player.strength,
        user_luk=player.luck,
        move_power=10,  # Example move power
        target_def=opponent.defense
    )

    # Update opponent's HP
    opponent_hp -= damage
    if opponent_hp < 0:
        opponent_hp = 0

    # Update battle state
    if battle.player_id_1 == player.player_id:
        battle.hp_remaining_2 = opponent_hp
    else:
        battle.hp_remaining_1 = opponent_hp
    db.session.commit()

    # Check for victory
    if opponent_hp == 0:
        # End the battle
        end_battle(battle.battle_id)
        return jsonify(response_type='in_channel', text=f'<@{user_id}> defeated <@{opponent.slack_user_id}>!')
    else:
        return jsonify(response_type='in_channel', text=f'<@{user_id}> attacked <@{opponent.slack_user_id}> for {damage} damage!')
