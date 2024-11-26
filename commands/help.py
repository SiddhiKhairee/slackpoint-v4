from copy import deepcopy


class Help:
    """
    This class handles the Help functionality.
    """

    commands_dictionary = {}

    command_help = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "{command_help}"},
    }

    def __init__(self):
        """
        Constructor to initialize command dictionary and payload object

        :param:
        :type:
        :raise:
        :return: None
        :rtype: None

        """
        self.commands_dictionary["createtask"] = [
            "*Create Task*",
            ">To create a task, just try the command */create-task* and you would receive a message from Slack to fill out the details of the task.\n>Enter the description, deadline and the points of the task.\n>For example:\n>*Description*: Hey! This is my new task\n>*Deadline*: 12/31/2022 (just select a date from the date picker)\n>*Points*: 5 (select a point from 1 to 5)\n>And that's it! You should receive a reply from Slack with the generated *Task ID*.",
        ]
        self.commands_dictionary["viewcompleted"] = [
            "*View Completed Tasks*",
            ">To view completed tasks, just try the command */view-completed*, and there you go! SlackPoint would show you a list of completed tasks.",
        ]
        self.commands_dictionary["viewpending"] = [
            "*View Pending Tasks*",
            ">To view pending tasks, just try the command */view-pending*, and there you go! SlackPoint would show you a list of pending tasks.",
        ]
        self.commands_dictionary["leaderboard"] = [
            "*Leaderboard*",
            ">To view the leaderboard, just try the command */leaderboard*, and SlackPoint would show you the top five contenders!",
        ]
        self.commands_dictionary["taskdone"] = [
            "*Complete Task*",
            ">To mark a task as Completed, just try the command */task-done* <Task ID>, and you can earn the points for the task.",
        ]
        self.commands_dictionary["help"] = [
            "*Help*",
            ">Well, you are viewing it. You don't need my help in that case :D",
        ]
        self.commands_dictionary["edittask"] = [
            "*Edit Task*",
            ">To edit a task, just try the command */edit-task* <Task ID> and you would receive a message from Slack to update the details of the task.\n>Enter the description, deadline and the points of the task.\n>For example:\n>*Description*: Hey! This is my edited task\n>*Deadline*: 12/15/2022 (just select a date from the date picker)\n>*Points*: 5 (select a point from 1 to 5)\n>And that's it! You should receive a reply from Slack with the success message.",
        ]
        self.commands_dictionary["summary"] = [
            "*Summary*",
            ">To view the summary, just try the command */summary*, and there you go! SlackPoint would show you a list of pending tasks, completed tasks and the current leaderboard.",
        ]
        self.commands_dictionary["showstore"] = [
            "*Show the product in store and you can also buy it*",
            ">To view the products in the store, just try the command */show-store*, and there you go! SlackPoint would show you a list of products available in the store. In addition, you can buy the product by using the points you have earned.",
        ]
        self.commands_dictionary["createpet"] = [
            "*Create Pet*",
            ">To create a pet, just try the command */create-pet* and you would receive a message from Slack to fill out the details of the pet.\n>Enter the name of the pet. \n Each user can have only one pet.",        
        ]
        self.commands_dictionary["feedpet"] = [
            "*Feed Pet*",
            ">To feed your pet, just try the command */feed-pet* and you would need to select the food item from the list. \n Each food item will increase the pet's hunger level by a different amount.",
        ]
        self.commands_dictionary["showInventory"] = [
            "*Show Inventory*",
            ">To view the inventory, just try the command */show-inventory*, and there you go! SlackPoint would show you a list of items you have in the inventory.",
        ]
        self.commands_dictionary["pomodorotimer"] = [
            "*Pomodoro Timer*",
            ">To start a Pomodoro Timer, just try the command */pomodoro-timer* and you would receive a message from Slack to select the duration of the timer.\n>Once the timer is started, you can see the countdown in the message itself.",
        ]
        self.commands_dictionary["createcharacter"] = [
            "*Character Creation*",
            ">To create a character, use the */create-character* command. Customize the stats as you please, but you can only allocate 20 points total.\n"
            ">So, keep that in mind as you customize your character.\n\n"
            ">*Character Class:* This determines the types of moves your character can use in battle, each class having its own set.\n\n"
            ">*Strength (STR)*: The amount of strength a character has represents the amount of physical strength it has\n"
            ">*Magic (MAG)*: The amount of magic prowess a character has to use magic attacks\n"
            ">*Defense (DEF)*: A value used to reduce the amount of damage done by physical attacks\n"
            ">*Resistance (RES)*: A value used to reduce the amount of damage done by magical attacks\n"
            ">*Agility (AGL)*: A value used to determine the hit rate and dodge rate of the character. Whoever has more agility will get the first turn in battle.\n"
            ">*Luck (LUK)*: A value used to slightly influence the chance to hit and dodge. It also factors into any RNG-based decisions that may occur during battle\n",
        ]
        self.commands_dictionary["allocatepoints"] = [
            "*Allocate Points*",
            ">To reallocate stats, use the */allocate-points* command. Customize the stats as you please, but you can only allocate as much as you currently have + any points you have in reserve.\n"
            ">So, keep that in mind as you customize your character.\n",
        ]
        self.commands_dictionary["filtertasks"] = [
            "*Filter Tasks*",
            ">To filter a task, just try the command */filtertasks*, and you can filter them based on the tags.",
        ]
        self.payload = {"response_type": "ephemeral", "blocks": []}

    def help_all(self):
        """
        Creates a payload with the help details for all commands

        :param:
        :type:
        :raise:
        :return: Payload object containing helper details of all commands
        :rtype: dict[str, Any]

        """
        response_payload = deepcopy(self.payload)
        for name in self.commands_dictionary.keys():
            blocks = self.help(name)
            response_payload["blocks"].extend(blocks)
        return response_payload

    def help(self, command_name):
        """
        Creates a payload blocks for particular command

        :param command_name: Command name
        :type command_name: str
        :raise:
        :return: Blocks list containing details of a particular command provided in parameter
        :rtype: list

        """
        blocks = []
        command_name_block = deepcopy(self.command_help)
        command_help_desc_block = deepcopy(self.command_help)
        command_help = self.commands_dictionary.get(command_name)
        command_name_block["text"]["text"] = command_name_block["text"]["text"].format(
            command_help=command_help[0]
        )
        command_help_desc_block["text"]["text"] = command_help_desc_block["text"][
            "text"
        ].format(command_help=command_help[1])

        blocks.append(command_name_block)
        blocks.append(command_help_desc_block)
        return blocks
