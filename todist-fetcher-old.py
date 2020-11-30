# Denne virker! Men spør Notion API hver gang og det er unødvendig.

from notion.client import NotionClient
from todoist.api import TodoistAPI
from datetime import datetime as dt
import threading

# Helper functions
def fetch_project_tasks(project_id, api):
    tasks = []
    for task in api.state['items']:
        if task['project_id'] == project_id:
            tasks.append(task)
    return tasks

def extract_task_value(value, task_list):
    return [task_list[i][value] for i in range (0,len(task_list))]   


def send_todoist_to_notion():
    print('')
    print(f"{dt.utcnow()} – Checking for new tasks in Todoist")
    threading.Timer(15.0, send_todoist_to_notion).start()   

    # 1) Connecting to APIs
    # 1.1) CONNECT AND SYNC WITH TODOIST API
    todoist_api = TodoistAPI('ba528c7dd9b832bdd9ef71a85001be3ee7e6c8b0')
    todoist_api.sync()

    # 1.2) CONNECT AND SYNCT WITH NOTION API
    notion_client = NotionClient(token_v2="39ef1ddd36f6d1df766f496a75449093fadf1aa6c4c1e3442602754bc82c918a032bc025d4c5956801b58bc88fe10d950b6e844fa24b1951a095c3dde43a37ca7a509f77169389a97a70dc74baf5")
    notion_url = 'https://www.notion.so/3457774311c54092b2dc4e0693e638bd?v=430b979a9640427185c9f9a3460b2fdf'

    notion_query = notion_client.get_collection_view(notion_url)
    # 2) Fetching all info from todoist inbox
    tasks_dump = fetch_project_tasks(2250036208, todoist_api)

    # 2.1) Lists with dicts of task ID and content only 
    tasks = [{tasks_dump[i]['id']:tasks_dump[i]['content']} for i in range (0,len(tasks_dump))]
    todoist_ids = extract_task_value('id', tasks_dump)

    # 3) Fetching todist task ids in notion inbox 
    notion_ids = list(map(int, filter(lambda x: x != '', [row.todoist_id for row in notion_query.collection.get_rows()])))
    new_tasks = [new_id for new_id in todoist_ids if new_id not in notion_ids]

    # 4) Pushing new tasks to Todoist
    if new_tasks:
        print(f"{dt.utcnow()} – Found new task(s), pushing to Notion")
        for new_task in new_tasks:
            for i in range(0, len(tasks)):
                if new_task in tasks[i]:
                    print(f"{dt.utcnow()} – New task added from todoist. ID: " + str(new_task) + ', Content:  ' + tasks[i][new_task])
                    row = notion_query.collection.add_row()
                    row.todoist_id = str(new_task)
                    row.name = tasks[i][new_task]
                    row.todoist = 'JA'

# Starting cron job
send_todoist_to_notion()                    
        