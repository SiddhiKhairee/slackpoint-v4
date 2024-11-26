# Installation Instructions

This project is somewhat unique in how it is run since it is a bot that operates using the the Slack Bot API and hosted via the ngrok shell.

## 📖 Getting Started

Below are the tools and software that you will need in order to run the project. Please ensure that all of these are installed before you start
on the implementation:

### Prerequisites:
  - Download [Python3.x](https://www.python.org/downloads/) (Our team is using Python 3.10, but you can adapt to any Python version if you desire).
  - Download [Flask](https://flask.palletsprojects.com/en/2.2.x/installation/).
  - Download [PostgreSQL](https://www.postgresql.org/download/)
  - Download [pgAdmin](https://www.pgadmin.org/download/)
  - Download [ngrok](https://ngrok.com/)

## Creating a Virtual Environment

Create a virtual environment to install all the packages in (this example's installation uses `.venv` as an example name,
but feel free to use something else if you would like to):

```bash
  python3.x -m venv .venv
```

### Activate the virtual environment:

**Linux/MacOS:**
```bash
  source .venv/bin/activate
```

**Windows:**
```bash
  .venv/Scripts/activate
```

**Clone the project from GitHub:**

```bash
  git clone https://github.com/brianhhuynh38/slackpoint-v3
```

**Go to the project directory:**

```bash
  cd Slackpoint
```

**Install dependencies:**

```bash 
  pip install -r requirements.txt
```

You may run into some issues when installing dependencies; this could be due to a variety of factors, but is mostly likely caused by 
version conflicts between the packages, or due to missing packages that the project might need. If you get an error while trying to 
compile the project, please make sure that all of the packages you need are installed by using the stack trace to figure out what
packages you might need to install.

## Create Your Slack Bot

The process of creating your Slack Bot should not be too difficult, but we will walk you through the process as it may be difficult to 
figure out where exactly each component is.

### 1. Register/Log In to the [Slack API Website](https://api.slack.com/)

The [Slack API website](https://api.slack.com/) allows you to manage the settings for your Slack Bot. Create an account or log into your Slack account
in order to be able to create Slack apps that we will be deploying later in this guide.

### 2. Create a Slack Workspace

You must also have a designated Slack workspace in order to invite teammates and SlackPoint into so that you are able to test the program.
If you already have a workspace you would like to use: fantastic! You can move onto the next step if so. Otherwise, create a Slack workspace
by logging in at [Slack](https://slack.com/) and selecting `Create a New Workspace`. From there, simply follow the instructions provided to create and name
the workspace.

![image](https://github.com/user-attachments/assets/362d62ba-d208-443a-8994-497d78663528)


### 3. Create New Slack App

Navigate to the Slack Bot Dashboard under the `Your Apps` tab in the navigation bar. You should be brought to the page depicted below:

![image](https://github.com/user-attachments/assets/3e750e9e-7103-4758-9bdf-5dfe5fdbf81e)

From here, select the `Create New App` button at the top right. Choose to create an app from scratch, then name your bot and assign it to 
the workspace added in the previous step. You have now created your Slack Bot

## Running Your Slack Bot

This implementation is deployed using the ngrok shell, which generates a domain that is able to used as an interactive endpoint for each 
of your Slack bot's commands and overall functionality.

There are two methods in which you can use to run the ngrok shell: generating a new domain every time you use the ngrok shell and using the
free static domain that is provided to every user on ngrok.com. I would also like to note that both of these methods require registration on
ngrok.com in order to authenticate the shell.

### New Domain

I would highly recommend against doing this method (though it is the method used by the team before us), but this is simple, but tedious, to set up.
It simply requires you to open the ngrok shell, then type the following into the terminal:

```bash
ngrok http 5000
```

This allows you to use the generated domain name in order to host your Slack bot locally. However, this method comes with a major drawback: the URL
generated from the ngrok shell changes every single time you do this. In other words, you will have to replace this endpoint link in your bot every 
single time you generate a new link. I highly recommend you try the option with the static domain.

### Static Domain

When creating a new ngrok account, it will give each user the option to claim their own static domain. However, you will not be able to customize it, 
nor will you be able to create more than one. On the plus side, this domain will not change like the other option, making it so that you would not have 
to constantly replace your interactive endpoints every single time you want to run the program. The static domain can be claimed from the ngrok domain 
dashboard. After claiming your domain, enter the following into the ngrok shell:

```bash
ngrok http --url=[Your static domain] 5000
```

This generates a link for you to use, like the last method, but should just be your static domain. It is still hosted on localhost:5000 as well.

## Set Up The Slack Bot

After generating your ngrok shell url, you can now use it to link up your Slack bot and all the slash commands.
There are several categories that need to be filled out when creating your Slack bot. Let's go over them one by one:

### 1. Filling Out Interactivity and Shortcuts

This section is necessary to establish the interactivity between Slack and you bot. The link should use the IP address generated by ngrok
with the addition of `/slack/interactive-endpoint` to the end.

![image](https://github.com/user-attachments/assets/ec4985d2-015a-4b92-a1c5-c6ae0142be77)

### 2. Filling Out the Slash Commands

This will set up endpoints for each of the commands to be used for your Slack bot. You will need to create each slash command that you would
like to use for your implementation. Each slash command requires you to identify a link, which should looks something like this:

```
[ngrok IP]/[command route]
```

To provide a specific example, if we were trying to write the link for the create-task function, it would look something like this:

```
https://my-ngrok-ip-thing/create
```

Be sure to provide descriptions and usability instructions for each of your commands so that your users also know how to use each command.
If you are using the New Domain method, you will have to replace the ngrok IPs in both of these steps for every command and the interactivity
and shortcuts section every time you would like to run this.

![image](https://github.com/user-attachments/assets/5eaeb9e8-86ec-4d05-a932-112965dfe115)

Be aware that the Request URL:

For example, for the `/create-task` function, inside the code(app.py) is called `/create` so you should use `https://my-ngrok-ip-thing/create` not `https://my-ngrok-ip-thing/create-task`! You should also check all ther command to make sure it's correct!


## Setting Up the `.env` File

Before running your application and creating the database for the server, the Slack bot's verification tokens and secrets must be defined.
This information can be found in the Basic Information section of the Slack Bot API dashboard, pictured here:

![image](https://github.com/user-attachments/assets/945722a4-b6e7-45cc-a3c3-ed8c37f9a6f1)

In the source code, create a `.env` file in the root folder of the project. This defines the token variables required for authorization to the 
Slack API. Here is an example of the file below:

```
DATABASE_URL = "postgresql://postgres:SlackDBWorkPls@localhost:5432/SlackPoint"
# SLACK API key:
SLACK_SIGNING_SECRET = "Signing Secret in Basic Information"
SLACK_BOT_TOKEN = "Bot Token in Install App"
VERIFICATION_TOKEN = "Verification Token in Basic Information"
```

You may have noticed that there is also a database URL defined as one of the `os` variables. We'll be covering that in the next step.

## Setting Up the Database

To create the database, you can use pgAdmin to make the process of making the database much easier. On Mac, there should also be external tools 
that allow pgAdmin to run as well.

(1) Create a database in pgAdmin with any name convention.
  
(2) Change the local path of PostgreSQL in the `.env` file (DATABASE_URL= 'postgresql://postgres:(password)@localhost/(database name from PgAdmin') 

To create tables in the database,
```bash
flask before_start
```

## Running the Server

Now you have all the materials you need in order to run the server:

```bash
  flask run
  Site will be hosted at:
      http://127.0.0.1:5000/
```

From here, your Slack bot should be functional as long as you have followed all of these steps. I would try to use the `/help` command to see if the 
bot is working properly.
       
