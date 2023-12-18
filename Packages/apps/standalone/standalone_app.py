import sys
from PySide2.QtWidgets import QApplication
from Packages.apps.standalone.main_window_standalone import MainWindowStandalone
from Packages.utils.logger import init_logger

logger = init_logger(__file__)

class PinpinApp(QApplication):
    
    def __init__(self, argv = sys.argv):
        super(PinpinApp, self).__init__(argv)
        self.window = MainWindowStandalone()

        logger.info('Create standalone main window.')
