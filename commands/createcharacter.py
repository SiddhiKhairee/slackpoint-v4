

class CreateCharacter:
    """
    This class handles all functionality related to the creation of player characters.
    """

    base_create_character_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">{greeting}! Your character CH-{id} was created successfully.",
        },
    }

    greetings = ["Awesome", "Great", "Congratulations", "Well done", "Let's go"]

    def __init__(self):
        """
        Constructor to initialize payload object

        :param:
        :type:
        :raise:
        :return: None
        :rtype: None

        """
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }

    def create_task_input_blocks(self):
        """
        Create blocks list containing input fields for description, deadline, points of a task, along with a button to create the task

        :param:
        :type:
        :raise:
        :return: Blocks list
        :rtype: list

        """
        block_description = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_action_description",
            },
            "label": {"type": "plain_text", "text": "Description", "emoji": True},
        }
        block_class_selection = {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {"type": "plain_text", "text": "Select", "emoji": True},
                "options": [
                    {
                        "text": {"type": "plain_text", "text": "Swordmaster", "emoji": False},
                        "value": "Swordmaster",
                    },
                    {
                        "text": {"type": "plain_text", "text": "Fire Mage", "emoji": False},
                        "value": "Fire Mage",
                    }
                ],
                "action_id": "create_action_points",
            },
            "label": {"type": "plain_text", "text": "Points", "emoji": True},
        }
        block_actions_button = {
            "type": "button",
            "text": {
                "type": "plain_text", 
                "text": "Create task"
            },
            "action_id": "create_action_button",
        }
        block_actions = {"type": "actions", "elements": []}
        block_actions["elements"].append(block_actions_button)

        blocks = []
        blocks.append(block_description)
        blocks.append(block_deadline)
        blocks.append(block_points)
        blocks.append(block_actions)
        return blocks

    def create_task(self, desc, points, deadline):
        """
        Creates a task in database and returns payload with success message along with the newly created Task ID

        :param desc: Description of task
        :type desc: str
        :param points: Points of task
        :type points: int
        :param deadline: Deadline of task
        :type deadline: Date
        :raise:
        :return: Blocks list of response payload
        :rtype: list

        """
        # DB call to add task, returns id
        task = Task()
        task.description = desc
        task.points = points
        task.deadline = deadline
        db.session.add(task)
        db.session.commit()
        db.session.refresh(task)

        # task id
        id = task.task_id

        # add the task in assignment, without user assignment
        assignment = Assignment()
        assignment.assignment_id = id
        assignment.progress = 0
        db.session.add(assignment)
        db.session.commit()

        response = deepcopy(self.base_create_task_block_format)
        response["text"]["text"] = response["text"]["text"].format(greeting=random.choice(self.greetings), id=id)
        self.payload["blocks"].append(response)
        return self.payload["blocks"]