import sys
sys.stdout = open('output.log', 'w')

path = r'D:\Pinpin'
sys.path.append(path)

from Packages.apps.houdini.ui.houdini_class import HoudiniPinpin
ui = HoudiniPinpin()
