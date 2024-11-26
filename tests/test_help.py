from commands.help import Help


def test_help():
    """
    Test the help command

    :param:
    :type:
    :raise:
    :return: Assert if test case executed successfully
    :rtype: bool

    """

    # test function
    h = Help()
    payload = h.help_all()

    # expectation
    expected_payload = {
        "response_type": "ephemeral",
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Create Task*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To create a task, just try the command */create-task* and you would receive a message from Slack to fill out the details of the task.\n>Enter the description, deadline and the points of the task.\n>For example:\n>*Description*: Hey! This is my new task\n>*Deadline*: 12/31/2022 (just select a date from the date picker)\n>*Points*: 5 (select a point from 1 to 5)\n>And that's it! You should receive a reply from Slack with the generated *Task ID*.",
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*View Completed Tasks*"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To view completed tasks, just try the command */view-completed*, and there you go! SlackPoint would show you a list of completed tasks.",
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*View Pending Tasks*"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To view pending tasks, just try the command */view-pending*, and there you go! SlackPoint would show you a list of pending tasks.",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Leaderboard*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To view the leaderboard, just try the command */leaderboard*, and SlackPoint would show you the top five contenders!",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Complete Task*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To mark a task as Completed, just try the command */task-done* <Task ID>, and you can earn the points for the task.",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Help*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">Well, you are viewing it. You don't need my help in that case :D",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Edit Task*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To edit a task, just try the command */edit-task* <Task ID> and you would receive a message from Slack to update the details of the task.\n>Enter the description, deadline and the points of the task.\n>For example:\n>*Description*: Hey! This is my edited task\n>*Deadline*: 12/15/2022 (just select a date from the date picker)\n>*Points*: 5 (select a point from 1 to 5)\n>And that's it! You should receive a reply from Slack with the success message.",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Summary*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To view the summary, just try the command */summary*, and there you go! SlackPoint would show you a list of pending tasks, completed tasks and the current leaderboard.",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Show the product in store and you can also buy it*",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To view the products in the store, just try the command */show-store*, and there you go! SlackPoint would show you a list of products available in the store. In addition, you can buy the product by using the points you have earned.",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Create Pet*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To create a pet, just try the command */create-pet* and you would receive a message from Slack to fill out the details of the pet.\n>Enter the name of the pet. \n Each user can have only one pet.",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Feed Pet*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To feed your pet, just try the command */feed-pet* and you would need to select the food item from the list. \n Each food item will increase the pet's hunger level by a different amount.",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Show Inventory*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To view the inventory, just try the command */show-inventory*, and there you go! SlackPoint would show you a list of items you have in the inventory.",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Pomodoro Timer*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To start a Pomodoro Timer, just try the command */pomodoro-timer* and you would receive a message from Slack to select the duration of the timer.\n>Once the timer is started, you can see the countdown in the message itself.",
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*Character Creation*"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To create a character, use the */create-character* command. Customize the stats as you please, but you can only allocate 20 points total.\n>So, keep that in mind as you customize your character.\n\n>*Character Class:* This determines the types of moves your character can use in battle, each class having its own set.\n\n>*Strength (STR)*: The amount of strength a character has represents the amount of physical strength it has\n>*Magic (MAG)*: The amount of magic prowess a character has to use magic attacks\n>*Defense (DEF)*: A value used to reduce the amount of damage done by physical attacks\n>*Resistance (RES)*: A value used to reduce the amount of damage done by magical attacks\n>*Agility (AGL)*: A value used to determine the hit rate and dodge rate of the character. Whoever has more agility will get the first turn in battle.\n>*Luck (LUK)*: A value used to slightly influence the chance to hit and dodge. It also factors into any RNG-based decisions that may occur during battle\n",
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*Allocate Points*"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To reallocate stats, use the */allocate-points* command. Customize the stats as you please, but you can only allocate as much as you currently have + any points you have in reserve.\n>So, keep that in mind as you customize your character.\n",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Filter Tasks*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To filter a task, just try the command */filtertasks*, and you can filter them based on the tags.",
                },
            },
        ],
    }
    print(payload)
    print("\n\n\n")
    print(expected_payload)
    assert payload == expected_payload
