import maya.OpenMayaUI as omui
from PySide2.QtWidgets import QWidget
from shiboken2 import wrapInstance

def maya_main_window():
    """Return the Maya main window widget as a Python object.
    """
    
    main_window_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_pointer), QWidget)