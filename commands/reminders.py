from commands.viewpoints import ViewPoints
import datetime
import re

class Reminders:
    """
    This class handles the Create Reminder functionality.
    """
    def createReminder(self):
        '''
        Method to create reminder
        '''
        #Fetch pending task list
        vp = ViewPoints(progress=0.0)
        pending_tasks = vp.get_list()
        listofdict = pending_tasks["blocks"]
        tom_tasks=[]
        for taskinfo in listofdict:
            task_text = taskinfo["text"]["text"]
            str_date = re.findall("\d{4}-\d{2}-\d{2}",task_text)[0]
            curr_date = datetime.date.today()
            task_date=datetime.datetime.strptime(str_date,"%Y-%m-%d").date()
            tomorrow = curr_date + datetime.timedelta(days=1)
            if task_date==tomorrow:
                tom_tasks.append(task_text)
        return tom_tasks


    def reminder_msg_block(self,msg):
        '''
        Method to create message block
        Input - list of str
        Output - Slack block
        '''
        parent_msg = {"blocks": []}
        child_msg = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Reminder : Urgent Tasks Due Completion :*"
                }
            }

        parent_msg['blocks'].append(child_msg)
        for task_text in msg:
            child_msg = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": task_text
                 }
            }
            parent_msg['blocks'].append(child_msg)

        return parent_msg



