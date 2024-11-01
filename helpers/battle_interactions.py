from models import db, Battle, Player

def create_battle(player1_id, player2_id):
    # Retrieve player objects
    player1 = Player.query.get(player1_id)
    player2 = Player.query.get(player2_id)

    # Initialize HP and MP from players' max values
    battle = Battle(
        player_id_1=player1_id,
        hp_remaining_1=player1.max_hp,
        mp_remaining_1=player1.max_mp,
        player_id_2=player2_id,
        hp_remaining_2=player2.max_hp,
        mp_remaining_2=player2.max_mp
    )

    db.session.add(battle)
    db.session.commit()
    return battle

def update_battle(battle_id, hp1, mp1, hp2, mp2):
    battle = Battle.query.get(battle_id)
    battle.hp_remaining_1 = hp1
    battle.mp_remaining_1 = mp1
    battle.hp_remaining_2 = hp2
    battle.mp_remaining_2 = mp2
    db.session.commit()

def get_battle_by_player(player_id):
    battle = Battle.query.filter(
        (Battle.player_id_1 == player_id) | (Battle.player_id_2 == player_id)
    ).first()
    return battle

def end_battle(battle_id):
    battle = Battle.query.get(battle_id)
    db.session.delete(battle)
    db.session.commit()
