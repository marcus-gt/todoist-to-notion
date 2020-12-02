# Denne virker! Men spør Notion API hver gang og det er unødvendig.

from notion.client import NotionClient
from todoist.api import TodoistAPI
from datetime import datetime as dt
import threading
from utilities_docker import Notion, fetch_project_tasks, extract_task_value

#Initializers
notion_tasks = Notion()
todoist_api = TodoistAPI('ba528c7dd9b832bdd9ef71a85001be3ee7e6c8b0')

def send_todoist_to_notion(time_interval=15.0):
    print('')
    print(f"{dt.utcnow()} – Checking for new tasks in Todoist")
    threading.Timer(time_interval, send_todoist_to_notion).start()  

    # 1) Set notion IDs to current state
    notion_ids = notion_tasks.notion_data

    # 2) Sync with Todoist API
    todoist_api.sync()  

    # 3) Fetching all info from todoist inbox
    todoist_tasks_dump = fetch_project_tasks(2250036208, todoist_api)

    # 2.1) Lists with dicts of task ID and content only 
    all_todoist_tasks = [{todoist_tasks_dump[i]['id']:todoist_tasks_dump[i]['content']} for i in range (0,len(todoist_tasks_dump))]
    todoist_ids = extract_task_value('id', todoist_tasks_dump)    

    # 3) Checkoig Todoist tasks against Notion tasks for new tasks
    new_todoist_tasks = [new_id for new_id in todoist_ids if new_id not in notion_ids]

    # 4) Sending new tasks to Notion inbox
    if new_todoist_tasks:
        print(f"{dt.utcnow()} – Found new task(s), pushing to Notion...")
        notion_tasks.push_to_notion(new_todoist_tasks, all_todoist_tasks)


# Starting cron job
send_todoist_to_notion()                    
        