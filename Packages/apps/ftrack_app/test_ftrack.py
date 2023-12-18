import ftrack_api
from Packages.apps.ftrack_app.constants import *

"""SERVER_URL = 'https://esma-montpellier.ftrackapp.com/'
API_KEY = 'MmMyM2RkMDMtNDcyMC00MjFkLWJlN2ItOWE3NDUyODAxZDNiOjpiYzQ4NzkyOC1kMDc0LTQ3ZDUtYjA4NC1kOThlNGE4NGI2ODk'
API_USER = 'D.DELAUNAY@mtp.ecolescreatives.com'

session = ftrack_api.Session(
    server_url = SERVER_URL,
    api_key = API_KEY,
    api_user = API_USER
)

ftrack_project_name = 'coup_de_soleil'

project = session.query(f'Project where name is "{ftrack_project_name}"').one()
project_name = project['name']

user = session.query(f'User where username is "{session.api_user}"').one()

app_tasks = session.query(
    f'Task where project.name is "{ftrack_project_name}" and assignments any (resource.username = "{session.api_user}")'
).all()

'''for task in app_tasks:
    print(f'Task Name: {task["name"]}')
    print(f'Status: {task["status"]["name"]}')
    print(f'Priority: {task["priority"]["name"]}')
    print('---')'''

target_task_name = 'rig_body'
new_status_name = 'WIP'
parent_folder = 'Petru'

task = session.query(
    f'Task where project.name is "{ftrack_project_name}" and name is "{target_task_name}" and parent.name is "{parent_folder}"'
).one()

new_status = session.query(f'Status where name is "{new_status_name}"').one()

task['status'] = new_status
session.commit()

session.close()"""

def start_ftrack_session():
    session = ftrack_api.Session(server_url = SERVER_URL, api_key = API_KEY, api_user = API_USER)
    return session

def edit_task_status(task_name: str, parent_name: str, status_name: str, ftrack_project_name: str):
    
    session = start_ftrack_session()

    task = session.query(
        f'Task where project.name is "{ftrack_project_name}" and name is "{task_name}" and parent.name is "{parent_name}"'
    ).one()

    new_status = session.query(f'Status where name is "{status_name}"').one()

    task['status'] = new_status
    session.commit()
    session.close()
    
edit_task_status('rig_body', 'Chauve souris', 'WIP', 'coup_de_soleil')
