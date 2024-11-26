<img src = "https://user-images.githubusercontent.com/48649849/194794889-3d3dc808-25f7-4c91-bfd5-10f9294e2d41.png" width="1080" height="200"/> 
  
![This is an image](https://img.shields.io/badge/purpose-Software_Engineering-blue)
[![DOI](https://zenodo.org/badge/865072057.svg)](https://doi.org/10.5281/zenodo.14015968)
![](https://img.shields.io/badge/codestyle-pyflake-purple?labelColor=gray)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Github](https://img.shields.io/badge/language-python-red.svg)](https://docs.python.org/3/)
[![GitHub contributors](https://img.shields.io/github/contributors/brianhhuynh38/slackpoint-v3)](https://github.com/brianhhuynh38/slackpoint-v3/graphs/contributors/)

[![build](https://github.com/brianhhuynh38/slackpoint-v3/actions/workflows/codecov.yml/badge.svg)](https://github.com/brianhhuynh38/slackpoint-v3/actions)
[![GitHub top language](https://img.shields.io/github/languages/top/brianhhuynh38/slackpoint-v3)](https://docs.python.org/3/)
[![GitHub last commit](https://img.shields.io/github/last-commit/brianhhuynh38/slackpoint-v3)](https://github.com/brianhhuynh38/slackpoint-v3/commits/main)
[![codecov](https://codecov.io/gh/brianhhuynh38/slackpoint-v3/branch/main/graph/badge.svg?token=1H92SAVB5S)](https://codecov.io/gh/brianhhuynh38/slackpoint-v3)


Gamify your slack tasks! 💻


A lot of teams use Slack to get things done. However when you have ton of things to do with no short term rewards in sight, it gets difficult to check off those tasks. That's where SlackPoint comes to the rescue! SlackPoint aims to make work more fun and get people motivated to finish their tasks by gamifying Slack!

## Check out Slackpoint v1 and v2
Our friends had started on this journey of making tasks easy and fun!
We're continuing their work to make sure you don't slack off :wink:

- v1: Check them out [here](https://github.com/nehakale8/slackpoint)
- v2: Check them out [here](github.com/nihar4276/slackpoint-v2)

https://user-images.githubusercontent.com/21088141/205798073-2269309d-5a60-43f9-a20a-74532c862d66.mp4

## Demos

### Demo of Commands

[![](https://img.youtube.com/vi/RVLecAD7Zk0/0.jpg)](https://www.youtube.com/watch?v=RVLecAD7Zk0)

### Selling Point Video

[![](https://img.youtube.com/vi/ThgeL1FfqfM/0.jpg)](https://www.youtube.com/watch?v=ThgeL1FfqfM)

## Built with
  <img src = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" width="40" height="40"/> Flask
  <br/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" height="40" /> Python
  <br/>
 <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="40" height="40" /> PostgreSQL

### How do you use this?

List of miracles that SlackPoint can perform✨:

* Create a new task
* Mark task as done
* View pending tasks
* View completed tasks
* Check the leaderboard to see who's winning!
* Edit an existing task
* Get a daily summary delivered to you. Or view it when you want!
* Ask for help
* Create a player character
* Allocate task points to strengthen your character

With the addition of v4, Slackpoint can:

* Adopt a fun pet raising system to gamify all the tasks
* Implement pomodoro timer
* Allows assigning of tasks while creating a new task
* Allows reassigning of tasks while editing a task 

Let's go over some of these

#### **1. Create new task:**

You can create a new task by simple using the ``/create-task`` command. We ask for just a few more parameters in addition to that:

Command: ``/create``

![Create Task GIF](https://i.imgur.com/lUtX23a.gif)

This particular command will create a new task with the description as ``Hey! This is my new task`` having ``100`` points and a deadline of ``15th October 2022``

#### **2. Mark task as done:**

Here you can mark a task as completed. You just need to give the task ID as a parameter

Command: ``/task-done [task ID]``

Example:
``/task-done 10214``

![Task Done GIF](https://i.imgur.com/gOB6dVs.gif)

This will mark the task having task ID ``10214`` as completed. Further, updates records to show that this task is completed by user who posted this command

#### **3. View pending tasks:**

This command will return the list of incomplete tasks. Relax! no parameters required here

Command: ``/viewpending [no parameters]``

![View pending GIF](https://i.imgur.com/TAnNoSO.gif)

Above command will display a list of pending tasks

#### **4. View completed tasks:**

Like the above command this will return a list of completed tasks. No parameters here as well!

Command: ``/viewcompleted [no parameter]``

![View completed GIF](https://i.imgur.com/3SFQU2N.gif)

Above command will display a list of completed tasks

#### **5. Filter Tasks by Tag:**

This command will allow you to get only the tasks from a certain category. Need all "Programming" tasks? Simply follow the template below:

Command: ``/filtertasks [tag,tag,tag,tag,tag,...]``

![image](https://github.com/user-attachments/assets/59483ac5-99dd-411d-918a-1bda594e3479)

#### **7. Edit a task:**

Made a mistake while adding a task? No problem! 
Edit the task with values pre-populated as you had entered before. 

Command: ``/edit-task [task ID]``

![Edit GIF](https://user-images.githubusercontent.com/21088141/205816733-2bf10e44-baae-45d1-91f3-9a92d8123041.gif)


This particular command will edit your existing task with the description as ``Hey! This is my edited task`` having ``4`` points and a deadline of ``15th December 2022``

#### **9. Help:**

Newbie at using SlackPoint? You could use some help...

Command: ``/help [no parameters]``

![Help GIF](https://user-images.githubusercontent.com/21088141/205815812-8144bef2-73df-438c-a84a-6e322a09625a.gif)


This will provide you will all the available commands and how to use them.

## Project documentation

The `docs` folder incorporates all necessary documents and documentation in our project regarding its overall design. The sphinx documentation can be built by referencing our directions on the GitHub wiki regarding the compilation of the documentation: [Documentation Compilation Guide](https://github.com/brianhhuynh38/slackpoint-v3/wiki/Documentation-Compilation-Guide)

We have also defined much of our theoretical game design and database models in our GitHub Wiki pages as well under the [Game Design](https://github.com/brianhhuynh38/slackpoint-v3/wiki/Game-Design) section.

### Project Dependencies

* flask
* slackclient
* python-dotenv
* slackeventsapi
* flask-sqlalchemy
* psycopg2
* pytest
* pytest-mock
* black
* pylint
* coverage
* pytest-cov

### Future of this project

* **Progress of a task is currently binary.** It can be improved to allow a percentage progress improvement
* **Improve code coverage**
* **UI/UX:** Improve leaderboard command response to show gifs/graphs to further make the leaderboard more attractive and gamify it
* **In-Depth Battle System:** Currently, there is only a foundation for the battle system ready. This is free to be changed as per the wishes of any developer due to the implementation’s simplicity, in terms of game mechanics.
    * **Delay-Based:** Attacks use a delay-based battle system in which the type of attack determines how long it takes to take another action.
    * **Type-Weakness + Dynamic Turn-Based Systems:** Each player is able to take multiple turns and is able to expend turns to change their class. Turn count can be manipulated by exploiting weaknesses and resistances.
* **Deeper Gamification:**
    * Integrate deeper game mechanics into
 the system to provide more incentive
 to pursue Task Points.
    * Battle Systems: Encourage user
 interaction through text-based battles,
 building stats through experience from
 completing tasks and a predetermined
 character growth system.
    *Pet System: 
add more interaction with your pet
 add the actual picture of your pet
 your pet can join the battle system
 one user can have more than one
 pe

* **Team Formations and Tasks:** The introduction of teams would be greatly beneficial as most software development operates in teams.
    * Assign tasks to a group of people and be able to distribute points across them all to make task delegation more accurate
    * Teams can also be added to battle formations within the game design aspect to introduce more advanced gameplay mechanics and features, increasing activity between teammates.




### Chat Channel

<code><a href="https://join.slack.com/t/slackpoint-v4-sid/shared_invite/zt-2uxxz6yqr-SG7uOVg8IaDxSLnidkqF_w" target="_blank"><img height="30" width="100" src="https://user-images.githubusercontent.com/111834635/194175304-834d5663-b6bb-4e38-981d-98bc1bf028b8.png"></a></code>


### Our team
- Min Tin Tu, Sidharth Shambu, Siddhi Khaire
### Reach out to us!

