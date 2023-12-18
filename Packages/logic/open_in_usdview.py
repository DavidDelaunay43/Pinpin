import os
import subprocess
from Packages.utils.constants import ROOT_PATH

run_usdview_bat_path = os.path.join(ROOT_PATH, 'Scripts', 'run_usdview.bat')

def open_in_usd_view(file_path: str):
    '''
    '''

    batch_string = f"""@echo off
    cd /d "C:\\usdview\\scripts"
    usdview {file_path}
    """

    with open(run_usdview_bat_path, 'w') as fichier_batch:
        fichier_batch.write(batch_string)

        
    subprocess.call([run_usdview_bat_path], shell=True)
