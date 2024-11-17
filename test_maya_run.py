import os
import subprocess


"""mayapy_path: str = r'C:\Program Files\Autodesk\Maya2023\bin'
os.environ['PATH'] = os.environ['PATH'] + os.pathsep + mayapy_path
print(os.environ['PATH'])
subprocess.run(['test_maya.bat'], shell=True)
print('done')"""

subprocess.run(
    [
        r'C:\Program Files\Autodesk\Maya2023\bin\mayapy.exe',
        'test_maya.py'
    ]
)