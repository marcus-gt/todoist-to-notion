from notion.client import NotionClient
from todoist.api import TodoistAPI
from datetime import datetime as dt

# Helper functions
def fetch_project_tasks(project_id, api):
    tasks = []
    for task in api.state['items']:
        if task['project_id'] == project_id:
            tasks.append(task)
    return tasks

def extract_task_value(value, task_list):
    return [task_list[i][value] for i in range (0,len(task_list))]   

class Notion:
    def __init__(self):
        self.notion_data = self.get_notion_tasks()
    
    def get_notion_tasks(self):
        print(f"{dt.utcnow()} – Fetching all Todist tasks from Notion")
        self.notion_url = 'https://www.notion.so/3457774311c54092b2dc4e0693e638bd?v=430b979a9640427185c9f9a3460b2fdf'
        self.notion_client = NotionClient(token_v2="39ef1ddd36f6d1df766f496a75449093fadf1aa6c4c1e3442602754bc82c918a032bc025d4c5956801b58bc88fe10d950b6e844fa24b1951a095c3dde43a37ca7a509f77169389a97a70dc74baf5")
        self.notion_query = self.notion_client.get_collection_view(self.notion_url)
        notion_ids = list(map(int, filter(lambda x: x != '', [row.todoist_id for row in self.notion_query.collection.get_rows()])))
        return notion_ids
    
    def push_to_notion(self, new_todoist_tasks, all_todoist_tasks):
        if new_todoist_tasks:
            for new_task in new_todoist_tasks:
                for i in range(0, len(all_todoist_tasks)):
                    if new_task in all_todoist_tasks[i]:
                        print(f"{dt.utcnow()} – New task added from todoist. ID: " + str(new_task) + ', Content:  ' + all_todoist_tasks[i][new_task])
                        row = self.notion_query.collection.add_row()
                        row.todoist_id = str(new_task)
                        row.name = all_todoist_tasks[i][new_task]
                        row.todoist = 'JA' 
            # Update notion tasks
            self.notion_data = self.get_notion_tasks()