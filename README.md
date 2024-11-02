<img src = "https://user-images.githubusercontent.com/48649849/194794889-3d3dc808-25f7-4c91-bfd5-10f9294e2d41.png" width="1080" height="200"/> 
  
![This is an image](https://img.shields.io/badge/purpose-Software_Engineering-blue)
[![DOI](https://zenodo.org/badge/865072057.svg)](https://doi.org/10.5281/zenodo.14015968)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Github](https://img.shields.io/badge/language-python-red.svg)](https://docs.python.org/3/)
[![GitHub contributors](https://img.shields.io/github/contributors/brianhhuynh38/slackpoint-v3)](https://github.com/nihar4276/slackpoint-v2/graphs/contributors/)

[![build](https://github.com/smanishs175/WalletBuddy/actions/workflows/build.yml/badge.svg)](https://github.com/brianhhuynh38/slackpoint-v3/actions)
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

With the addition of v3, SlackPoint can also:

* Create a player character
* Allocate task points to strengthen your character
* Battle other players

Let's go over these one by one...

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

#### **5. Leaderboard:**

Want to get competitive? Take a peek at the leaderboard and try to beat the winner!

Command: ``/leaderboard [no parameters]``

![Leaderboard GIF](https://i.imgur.com/LNfVFHX.gif)

It displays the list of the top performers on the channel along with their points.

#### **6. Edit a task:**

Made a mistake while adding a task? No problem! 
Edit the task with values pre-populated as you had entered before. 

Command: ``/edit-task [task ID]``

![Edit GIF](https://user-images.githubusercontent.com/21088141/205816733-2bf10e44-baae-45d1-91f3-9a92d8123041.gif)


This particular command will edit your existing task with the description as ``Hey! This is my edited task`` having ``4`` points and a deadline of ``15th December 2022``

#### **7. Summary:**

Got too many tasks? Can't keep track of everything?
Now use the summary command to get a summarized version of all tasks and the leaderboard!
What's better? You get it delivered to your message box automatically every day!

Command: ``/summary [no parameters]``

![Summary GIF](https://user-images.githubusercontent.com/21088141/205815864-733197f6-cf83-4117-9118-bce0341c0533.gif)


This command will display a list of pending tasks, completed tasks, and the leaderboard. 

#### **8. Help:**

Newbie at using SlackPoint? You could use some help...

Command: ``/help [no parameters]``

![Help GIF](https://user-images.githubusercontent.com/21088141/205815812-8144bef2-73df-438c-a84a-6e322a09625a.gif)


This will provide you will all the available commands and how to use them. Same sh*t this section is doing.

## Project documentation
The `docs` folder incorporates all necessary documents and documentation in our project.
 
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

* Assign users to tasks while creating each task
* Add a command to reassign users
* Progress of a task is currently binary. It can be improved to allow a percentage progress improvement
* Improve code coverage
* UI/UX: Improve leaderboard command response to show gifs/graphs to further make the leaderboard more attractive and gamify it


## Developed by NC State students

Hey! We are a group of Graduate students at NC State University, or to be more specific, we are dreamers who want to be pioneers of the Computer Science world.
Consider this homework to be one of our many steps at achieving our dreams! :wink:


### Chat Channel

<code><a href="https://app.slack.com/client/T07PB5UGB7Y/C07PB5VLS30" target="_blank"><img height="30" width="100" src="https://user-images.githubusercontent.com/111834635/194175304-834d5663-b6bb-4e38-981d-98bc1bf028b8.png"></a></code>


### Our team
- Brian Huynh, Manav Kamdar, Shanmukh Chatadi
### Reach out to us!

