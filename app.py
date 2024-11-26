from commands.taskdone import TaskDone
from commands.leaderboard import Leaderboard
from flask import Flask, make_response, request, jsonify, Response
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from flask import Flask

from commands.help import Help
from commands.reminders import Reminders
from models import db
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from commands.showinventory import ShowInventory
from commands.battle_commands import handle_attack_command
from commands.battle_commands import handle_battle_command
from commands.viewpoints import ViewPoints
from configuration.env_config import Config
from commands.createtask import CreateTask
from commands.edittask import EditTask
from commands.summary import Summary
from commands.showstore import ShowStore
from commands.createcharacter import CreateCharacter
from commands.allocatepoints import AllocatePoints
from commands.filtertasks import FilterTasks
from commands.createpet import CreatePet

from models import Product
from helpers.errorhelper import ErrorHelper
from json import dumps
from helpers import helper



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
db.init_app(app)
migrate = Migrate(app, db)

# instantiating slack client
slack_client = WebClient(Config.SLACK_BOT_TOKEN)
slack_events_adapter = SlackEventAdapter(
    Config.SLACK_SIGNING_SECRET, "/slack/events", app
)
def add_default_products():
    # Check if the product table is empty
    if db.session.query(Product).count() == 0:
        # Add default products
        product1 = Product(name="Large food", price=3, description="Restores 3 HP")
        product2 = Product(name="Medium food", price=2, description="Restores 2 HP")
        product3 = Product(name="Small food", price=1, description="Restores 1 HP")
        db.session.add(product1)
        db.session.add(product2)
        db.session.add(product3)
        db.session.commit()

@app.cli.command("before_start")
@with_appcontext
def initialize_db():
    # Create the tables if they don't exist
    db.create_all()

    # Ensure the app context is available when adding products
    with app.app_context():
        add_default_products()

@app.route("/slack/interactive-endpoint", methods=["POST"])
def interactive_endpoint():
    """
    All interactive events like button click, input fields are received in this endpoint. We use this endpoint to handle the click event of 'Add task' button of create-task command.

    :param:
    :type:
    :raise:
    :return: Response object with 200 HTTP status
    :rtype: Response

    """
    payload = json.loads(request.form.get("payload"))
    if payload["type"] == "block_actions":
        actions = payload["actions"]
        if len(actions) > 0:
            if actions[0]["action_id"] == "create_action_button":
                # Create Task - button was clicked
                channel_id = payload["container"]["channel_id"]
                user_id = payload["user"]["id"]
                helper = ErrorHelper()
                ct = CreateTask()
                state_values = payload["state"]["values"]
                desc = None
                deadline = None
                points = None
                tags = None
                assignee = None
                for _, val in state_values.items():
                    if "create_action_description" in val:
                        desc = val["create_action_description"]["value"]
                    elif "create_action_deadline" in val:
                        deadline = val["create_action_deadline"]["selected_date"]
                    elif "create_action_tags" in val:
                        tags = val["create_action_tags"]["value"].split(",")
                    elif "create_action_points" in val:
                        if val["create_action_points"]["selected_option"] is not None:
                            points = val["create_action_points"]["selected_option"][
                                "value"
                            ]
                        else:
                            points = None
                    elif "create_action_assignee" in val:
                        assignee = val["create_action_assignee"]["selected_user"]
                if desc is None or deadline is None or points is None:
                    error_blocks = helper.get_error_payload_blocks("createtask")
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=error_blocks
                    )
                else:
                    blocks = ct.create_task(desc=desc, points=points, deadline=deadline, tags=tags, assignee=assignee)
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=blocks
                    )

            elif actions[0]["action_id"] == "edit_action_button":
                # Edit Task - button was clicked
                channel_id = payload["container"]["channel_id"]
                user_id = payload["user"]["id"]
                task_id = int(actions[0]["value"])
                helper = ErrorHelper()
                et = EditTask(task_id)
                state_values = payload["state"]["values"]
                desc = None
                deadline = None
                points = None
                tags = None
                assignee_slack_id = None
                for _, val in state_values.items():
                    if "edit_action_description" in val:
                        desc = val["edit_action_description"]["value"]
                    elif "edit_action_deadline" in val:
                        deadline = val["edit_action_deadline"]["selected_date"]
                    elif "create_action_tags" in val:
                        tags = val["create_action_tags"]["value"].split(",")
                    elif "edit_action_points" in val:
                        if val["edit_action_points"]["selected_option"] is not None:
                            points = val["edit_action_points"]["selected_option"][
                                "value"
                            ]
                        else:
                            points = None
                    elif "edit_action_assignee" in val:
                        assignee_slack_id = val["edit_action_assignee"]["selected_user"]
                if desc is None or deadline is None or points is None:
                    error_blocks = helper.get_error_payload_blocks("edittask")
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=error_blocks
                    )
                else:
                    blocks = et.edit_task(desc=desc, points=points, deadline=deadline, tags=tags, assignee_slack_id=assignee_slack_id)
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=blocks
                    )

            elif actions[0]["action_id"] == "create_character_button":
                # Create character - button was clicked
                channel_id = payload["container"]["channel_id"]
                user_id = payload["user"]["id"]
                helper = ErrorHelper()
                cc = CreateCharacter(user_id)
                state_values = payload["state"]["values"]

                character_class = None
                strength = None
                magic = None
                defense = None
                resistance = None
                agility = None
                luck = None

                # Looks through all character stats
                for _, val in state_values.items():
                    if "create_character_class" in val:
                        character_class = val["create_character_class"]["selected_option"]["value"]
                    if "create_character_strength" in val:
                        strength = int(val["create_character_strength"]["value"])
                    if "create_character_magic" in val:
                        magic = int(val["create_character_magic"]["value"])
                    if "create_character_defense" in val:
                        defense = int(val["create_character_defense"]["value"])
                    if "create_character_resistance" in val:
                        resistance = int(val["create_character_resistance"]["value"])
                    if "create_character_agility" in val:
                        agility = int(val["create_character_agility"]["value"])
                    if "create_character_luck" in val:
                        luck = int(val["create_character_luck"]["value"])

                # Checks if all fields are populated and if the total does not exceed 20
                if (all(stat is None for stat in [character_class, strength, magic, defense, resistance, agility, luck])
                        or strength + magic + defense + resistance + agility + luck > 20):
                    # Get error payload if any fields are empty or the stat total is over 20
                    error_blocks = helper.get_error_payload_blocks("createcharacter")
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=error_blocks
                    )
                else:
                    blocks = cc.create_character(
                        character_class=character_class,
                        strength=strength,
                        magic=magic,
                        defense=defense,
                        resistance=resistance,
                        agility=agility,
                        luck=luck
                    )
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=blocks
                    )

            elif actions[0]["action_id"] == "allocate_points_button":
                # Create character - button was clicked
                channel_id = payload["container"]["channel_id"]
                user_id = payload["user"]["id"]
                helper = ErrorHelper()
                ap = AllocatePoints(user_id)
                stat_total_boundary = ap.get_stat_total()
                state_values = payload["state"]["values"]

                character_class = None
                strength = None
                magic = None
                defense = None
                resistance = None
                agility = None
                luck = None

                # Looks through all character stats
                for _, val in state_values.items():
                    if "allocate_points_class" in val:
                        character_class = val["allocate_points_class"]["selected_option"]["value"]
                    if "allocate_points_strength" in val:
                        strength = int(val["allocate_points_strength"]["value"])
                    if "allocate_points_magic" in val:
                        magic = int(val["allocate_points_magic"]["value"])
                    if "allocate_points_defense" in val:
                        defense = int(val["allocate_points_defense"]["value"])
                    if "allocate_points_resistance" in val:
                        resistance = int(val["allocate_points_resistance"]["value"])
                    if "allocate_points_agility" in val:
                        agility = int(val["allocate_points_agility"]["value"])
                    if "allocate_points_luck" in val:
                        luck = int(val["allocate_points_luck"]["value"])

                # Checks if all fields are populated and if the total does not exceed the stat total boundary
                if (all(stat is None for stat in [character_class, strength, magic, defense, resistance, agility, luck])
                        or strength + magic + defense + resistance + agility + luck > stat_total_boundary):
                    # Get error payload if any fields are empty or exceeds the stat boundary
                    error_blocks = helper.get_error_payload_blocks("allocatepoints")
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=error_blocks
                    )
                else:
                    blocks = ap.allocate_points(
                        character_class=character_class,
                        strength=strength,
                        magic=magic,
                        defense=defense,
                        resistance=resistance,
                        agility=agility,
                        luck=luck
                    )
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=blocks
                    )
            elif actions[0]["action_id"] == "create_pet_action_button":
                # Create Pet - button was clicked
                channel_id = payload["container"]["channel_id"]
                user_id = payload["user"]["id"]
                helper = ErrorHelper()
                ct = CreatePet()
                state_values = payload["state"]["values"]
                pet_name = None
                for _, val in state_values.items():
                    if "create_action_pet_name" in val:
                        pet_name = val["create_action_pet_name"]["value"]
                if pet_name is None:
                    error_blocks = helper.get_error_payload_blocks("create-pet")
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=error_blocks
                    )
                else:
                    blocks = ct.create_pet(pet_name=pet_name, slack_user_id=user_id)
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=blocks)

    return make_response("", 200)


@app.route("/")
def basic():
    """
    Health check endpoint

    :param:
    :type:
    :raise:
    :return: 'Hello World' - the official health check response text
    :rtype: str

    """
    return "Hello World"


@app.route("/viewpending", methods=["POST"])
def vpending():
    """
    Endpoint to view the pending tasks

    :param:
    :type:
    :raise:
    :return: Response object with payload object containing details of pending tasks
    :rtype: Response

    """
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    text = data.get("text")

    vp = ViewPoints(progress=0.0)
    payload = vp.get_list()

    return jsonify(payload)


@app.route("/viewcompleted", methods=["POST"])
def vcompleted():
    """
    Endpoint to view the completed tasks

    :param:
    :type:
    :raise:
    :return: Response object with payload object containing details of completed tasks
    :rtype: Response

    """

    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    text = data.get("text")

    vp = ViewPoints(progress=1.0)
    payload = vp.get_list()

    return jsonify(payload)


@app.route("/filtertasks", methods=["POST"])
def filtertasks():
    """
    Endpoint to view the completed tasks

    :param:
    :type:
    :raise:
    :return: Response object with filtered tasks
    :rtype: Response

    """

    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    filters = data.get("text")
    tags = filters.split(',')

    ft = FilterTasks(tags)
    payload = ft.filter_tasks()

    return jsonify(payload)


@app.route("/taskdone", methods=["POST"])
def taskdone():
    """
    Endpoint to mark a task as completed

    :param:
    :type:
    :raise:
    :return: Response object with payload containing task completion message
    :rtype: Response

    """

    data = request.form
    td = TaskDone(data)
    payload = td.update_points()
    return jsonify(payload)



@app.route("/showstore", methods=["POST"])
def showstore():
    """
    Endpoint to view the store

    :param:
    :type:
    :raise:
    :return: Response object with payload object containing details of items in the store
    :rtype: Response

    """
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    blocks = ShowStore().create_show_store_blocks()
    slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks, text="Store")    
    return Response(), 200

@app.route("/create", methods=["POST"])
def create():
    """
    Endpoint to create a new task, this endpoint triggers an ephemeral message for the user to enter task details for creation

    :param:
    :type:
    :raise:
    :return: Response object with 200 HTTP status
    :rtype: Response

    """

    ct = CreateTask()
    blocks = ct.create_task_input_blocks()

    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)
    return Response(), 200


@app.route("/help", methods=["POST"])
def help():
    """
    A helper endpoint to view all commands and how to use them

    :param:
    :type:
    :raise:
    :return: Response object with payload object containing details of all commands and how to use them
    :rtype: Response

    """

    h = Help()
    payload = h.help_all()
    return jsonify(payload)


@app.route("/leaderboard", methods=["POST"])
def leaderboard():
    """
    Endpoint to view the leaderboard

    :param:
    :type:
    :raise:
    :return: Response object with payload object containing details of champions leading the SlackPoint challenge
    :rtype: Response

    """
    payload = Leaderboard().view_leaderboard()
    return jsonify(payload)


@app.route("/summary", methods=["POST"])
def summary():
    """
    Endpoint to view the pending tasks , completed taks and leaderboard

    :param:
    :type:
    :raise:
    :return: Response object with the summary text to send
    :rtype: Response

    """

    return Summary().get_summary()


@app.route("/summary-cron", methods=["POST"])
def cron_summary():
    """
    Endpoint for the cronjob to automatically send summary after every X minutes/hours/seconds

    :param:
    :type:
    :raise:
    :return: Response object with payload object containing details of champions leading the SlackPoint challenge
    :rtype: Response

    """
    helper.send_slack_message(summary())
    return jsonify({"success": True})


@app.route("/edit", methods=["POST"])
def edit():
    """
    Endpoint to mark a task as completed

    :param:
    :type:
    :raise:
    :return: Response object with payload containing task completion message
    :rtype: Response

    """
    data = request.form
    task_id = int(data.get("text"))
    et = EditTask(task_id)
    allowed, error = et.is_editable()
    if not allowed:
        return jsonify(error)

    blocks = et.edit_task_input_blocks()
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)
    return Response(), 200


@app.route("/reminder-cron", methods=["POST"])
def cron_reminder():
    """
    Endpoint to send reminders for pending tasks with close deadline

    :param:
    :type:
    :raise:
    :return: Response object with payload object sent to slack channel
    :rtype: Response

    """
    rem = Reminders()
    msg = rem.createReminder()
    msg_block = rem.reminder_msg_block(msg)
    helper.send_slack_message(msg_block)
    return jsonify({"success": True})


@app.route("/create-character", methods=["POST"])
def create_character():
    """
    Endpoint that creates a character given several values representative of character stats. This
    should only be usable if the user does not already have a character
    """
    # Get payload blocks for character creation
    data = request.form
    user_id = data.get("user_id")
    cc = CreateCharacter(user_id)
    blocks = cc.create_character_input_blocks()

    # Check if player already exists, if it does
    allowed, error = cc.can_create_character()

    if not allowed:
        return jsonify(error)

    channel_id = data.get("channel_id")
    slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)
    return Response(), 200


@app.route("/allocate-points", methods=["POST"])
def allocate_points():
    """
    Endpoint that allows the user to allocate any points that they have accrued from completing tasks
    to their current stats.
    """
    # Get user information
    data = request.form
    user_id = data.get("user_id")
    ap = AllocatePoints(user_id)

    # Check if player already exists, if it does
    allowed, error = ap.can_allocate_points()

    if not allowed:
        return jsonify(error)

    # Get payload blocks
    blocks = ap.allocate_points_input_blocks()

    channel_id = data.get("channel_id")
    slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)
    return Response(), 200

@app.route("/create-pet", methods=["POST"])
def create_pet():
    """
    Endpoint that creates a pet for the user
    """
    ct = CreatePet()
    blocks = ct.create_pet_input_blocks()

    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)
    return Response(), 200

@app.route("/pet-status", methods=["POST"])
def check_pet_status():
    """
    Endpoint that allows the user to check the status of their pet
    """
    ct = CreatePet()
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")

    blocks = ct.show_pet_status(slack_user_id=user_id)

    slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)
    return Response(), 200


@app.route("/initiate-battle", methods=["POST"])
def initiate_battle():
    """
    Endpoint that allows the user to initiate battle with another player
    """


@app.route("/take-battle-action", methods=["POST"])
def take_battle_action():
    """
    Endpoint that allows the user to take an action in the battle that they are currently in. Sends
    an error message
    """


@app.route('/slack/commands', methods=['POST'])
def handle_commands():
    command = request.form.get('command')
    user_id = request.form.get('user_id')
    text = request.form.get('text')  # Contains command arguments

    if command == '/battle':
        return handle_battle_command(user_id, text)
    if command == '/attack':
        return handle_attack_command(user_id)


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
