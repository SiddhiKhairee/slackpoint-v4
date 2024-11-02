from models import User, Player

def get_player_by_slack_id(slack_user_id):
    user = User.query.filter_by(slack_user_id=slack_user_id).first()
    if user and user.player_id:
        player = Player.query.get(user.player_id)
        return player
    return None
