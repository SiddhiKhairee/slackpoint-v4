import sqlalchemy
from datetime import datetime
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    """
    This class is a database model for the Product entity.
    """

    __tablename__ = "product"

    product_id = db.Column(
        db.Integer, primary_key=True, unique=True, autoincrement=True
    )
    name = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.Text)

    __table_args__ = (db.UniqueConstraint("product_id"),)


class Inventory(db.Model):
    """
    This class is a database model for the Inventory entity.
    """

    __tablename__ = "inventory"

    inventory_id = db.Column(
        db.Integer, primary_key=True, unique=True, autoincrement=True
    )
    product_id = db.Column(db.Integer, ForeignKey("product.product_id"))
    user_id = db.Column(db.Integer, ForeignKey("user.user_id"))
    quantity = db.Column(db.Integer)

    __table_args__ = (db.UniqueConstraint("inventory_id"),)


class Task(db.Model):
    """
    This class is a database model for the Task entity.
    """

    __tablename__ = "task"

    task_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    description = db.Column(db.Text())
    points = db.Column(db.Integer)
    deadline = db.Column(db.Date)
    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime)
    tags = db.Column(db.JSON)

    __table_args__ = (db.UniqueConstraint("task_id"),)


class Assignment(db.Model):
    """
    This class is a database model for the Assignment entity.
    """

    __tablename__ = "assignment"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey("user.user_id"))
    assignment_id = db.Column(db.Integer, ForeignKey("task.task_id"), primary_key=True)
    progress = db.Column(db.Float)
    assignment_created_on = db.Column(db.DateTime, default=datetime.now())
    assignment_updated_on = db.Column(db.DateTime)


class User(db.Model):
    """
    This class is a database model for the User entity.
    """

    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slack_user_id = db.Column(db.String, unique=True)
    player_id = db.Column(db.Integer, ForeignKey("player.player_id"))
    points_earned = db.Column(db.Integer, default=0)

    __table_args__ = (db.UniqueConstraint("user_id"),)

    def create_user(slack_user_id):
        """
        Creates a new user in the database if slack_user_id does not already exist.

        :param slack_user_id: The Slack user ID of the user.
        :type slack_user_id: str
        :return: The user object.
        :rtype: User
        """
        user = User.query.filter_by(slack_user_id=slack_user_id).first()
        if user is None:
            user = User(slack_user_id=slack_user_id)
            db.session.add(user)
            db.session.commit()
        return user


class Player(db.Model):
    """
    This class is a database model for the Player entity. It stores character stats used in
    battle calculations and any progression points that the Player can use to strength themselves.
    """

    __tablename__ = "player"

    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    character_class = db.Column(db.String)
    max_hp = db.Column(db.Integer)
    max_mp = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    magic = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    resistance = db.Column(db.Integer)
    agility = db.Column(db.Integer)
    luck = db.Column(db.Integer)
    stat_points_to_allocate = db.Column(db.Integer)

    __table_args__ = (db.UniqueConstraint("player_id"),)


class Battle(db.Model):
    """
    This class is a database model for the Battle entity. This stores information on current Player
    status within a battle, mostly pertaining to their ID, HP, and MP. Currently there are two
    Players in any given Battle.
    """

    __tablename__ = "battle"

    # The ID number for the battle
    battle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # First player in the battle
    player_id_1 = db.Column(
        db.Integer, db.ForeignKey("player.player_id"), nullable=False
    )
    hp_remaining_1 = db.Column(db.Integer)
    mp_remaining_1 = db.Column(db.Integer)

    # Second player in the battle
    player_id_2 = db.Column(
        db.Integer, db.ForeignKey("player.player_id"), nullable=False
    )
    hp_remaining_2 = db.Column(db.Integer)
    mp_remaining_2 = db.Column(db.Integer)

    # Relationships
    player1 = db.relationship("Player", foreign_keys=[player_id_1])
    player2 = db.relationship("Player", foreign_keys=[player_id_2])

    __table_args__ = (db.UniqueConstraint("battle_id"),)


class Pet(db.Model):
    """
    This class is a database model for the Pet entity. This stores information on the Player's pet,
    including its name, type, and stats.
    """

    __tablename__ = "pet"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey("user.user_id"))
    pet_name = db.Column(db.String)
    hp = db.Column(db.Integer)

    __table_args__ = (db.UniqueConstraint("id"),)
