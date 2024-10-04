from pathlib import Path
import sys
from PySide2.QtWidgets import *
from Packages.ui.new.base_main_window import BaseMainWindow
from Packages.utils.core import Core


class StandaloneApp(QApplication):
    
    
    def __init__(self, project_path: Path, argv = sys.argv) -> None:
        super(StandaloneApp, self).__init__(argv)
        
        self.main_window: BaseMainWindow = BaseMainWindow(project_path=project_path)
        self.main_window.show()
        
        
def main() -> None:
    
    app = StandaloneApp(project_path=Core.current_project_path())
    app.exec_()
