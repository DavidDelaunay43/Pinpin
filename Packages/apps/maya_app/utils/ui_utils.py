from PySide2.QtWidgets import QWidget
from shiboken2 import wrapInstance
from maya.OpenMayaUI import MQtUtil


def mayaMainWindow():
    return wrapInstance(
        int(MQtUtil.mainWindow()), QWidget
    )
