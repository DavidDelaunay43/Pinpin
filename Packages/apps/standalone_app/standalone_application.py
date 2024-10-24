from pathlib import Path
import sys
from PySide2.QtWidgets import *
from Packages.apps.standalone_app.standalone_main_window import StandaloneMainWindow
from Packages.utils.core import Core


class StandaloneApp(QApplication):
    
    
    def __init__(self, project_path: Path, argv: list[str] = sys.argv) -> None:
        super(StandaloneApp, self).__init__(argv)
        
        self.main_window: StandaloneMainWindow = StandaloneMainWindow(project_path=project_path)
        self.main_window.show()
        
        
def main() -> None:
    
    app: StandaloneApp = StandaloneApp(project_path=Core.current_project_path())
    app.exec_()
