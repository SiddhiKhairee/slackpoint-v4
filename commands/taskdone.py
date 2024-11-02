from models import *
from helpers.errorhelper import ErrorHelper


class TaskDone:
    """
    This class handles the Task Completion functionality.
    """

    def __init__(self, data):
        """
        Constructor to initialize data and payload object

        :param:
        :type:
        :raise:
        :return: None
        :rtype: None

        """
        self.data = data
        self.payload = {
            "response_type": "ephemeral", 
            "blocks": []
        }

    # if get user id of given slack id/ create if not exists and return user id
    def get_or_create(self, uid):
        """
        Fetches user instance, generates the user if the user id is not present in DB

        :param uid: Slack User ID
        :type uid: str
        :raise:
        :return: instance of user fetched/generated from DB
        :rtype: Any

        """
        instance = db.session.query(User).filter_by(slack_user_id=uid).first()
        if instance:
            return instance
        else:
            instance = db.session.add(User(slack_user_id = uid))
            db.session.commit()
            return instance

    def update_points(self):
        """
        Marks the task as complete, validates whether the task exists and the task is yet to be completed

        :param:
        :type:
        :raise:
        :return: Success message on completion of task, Error message in case of failure of validation checks
        :rtype: str

        """
        helper = ErrorHelper()
        current_task_id = int(self.data.get('text'))
        current_slack_id = self.data.get('user_id')

        # check if task id exists
        exists = db.session.query(db.exists().where(Task.task_id == current_task_id)).scalar()

        task_progress = Assignment.query.filter_by(assignment_id=current_task_id, progress=0.0).all()

        if exists is False:
            return helper.get_command_help("no_task_id")

        # check if task is done
        elif exists is True and len(task_progress) == 0:
            return helper.get_command_help("task_already_done")
        # if task is not done

        elif exists is True and task_progress[0].progress == 0.0:

            my_query = self.get_or_create(current_slack_id)
            user_id = my_query.user_id

            # Increases the amount of points in Player if the User has a Player defined
            current_user = db.session.query(User).filter_by(slack_user_id=current_slack_id).one()
            self.p_id = getattr(current_user, "player_id")
            player_existent = self.p_id is not None

            if player_existent:
                # Get the current task and player
                curr_task = db.session.query(Task).filter_by(task_id=current_task_id).first()
                curr_player = db.session.query(Player).filter_by(player_id=getattr(my_query, "player_id")).first()
                # Update the values for the player
                db.session.query(Player).filter_by(player_id=getattr(curr_player, "player_id")).update(
                    dict(stat_points_to_allocate=getattr(curr_task, "points") + getattr(curr_player, "stat_points_to_allocate"))
                )

            db.session.query(Assignment).filter_by(assignment_id=current_task_id).update(dict(progress=1.0, user_id=user_id))
            db.session.commit()
            return helper.get_command_help("task_done")
