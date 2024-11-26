from models import *


def check_user_exists(userID):
    user = db.session.query(User).filter_by(slack_user_id=userID).first()
    if user is None:
        user = User(slack_user_id=userID)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    return user
