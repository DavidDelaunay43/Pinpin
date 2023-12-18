import ftrack_api 

session = ftrack_api.Session(
    server_url = 'https://esma-montpellier.ftrackapp.com/',
    api_key = 'MmMyM2RkMDMtNDcyMC00MjFkLWJlN2ItOWE3NDUyODAxZDNiOjpiYzQ4NzkyOC1kMDc0LTQ3ZDUtYjA4NC1kOThlNGE4NGI2ODk',
    api_user = 'D.DELAUNAY@mtp.ecolescreatives.com'
)

ftrack_project_name = 'coup_de_soleil'

project = session.query(f'Project where name is "{ftrack_project_name}"').one()
project_name = project['name']

for key in project.keys():
    print(key)

"""bougainvillier_item = project['asset']['3-items']['Vegetation']['Bougainvillier']
lookdev_task = bougainvillier_item['lookdev']

status = lookdev_task['status']['name']
print(f"Le statut de la tâche lookdev est : {status}")"""