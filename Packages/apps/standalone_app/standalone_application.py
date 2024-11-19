from pathlib import Path
import sys
from PySide2.QtWidgets import QApplication
from Packages.apps.standalone_app.standalone_main_window import StandaloneMainWindow
from Packages.utils.core import Core
from Packages.utils.init_pinpin import main as init_pinpin


class StandaloneApp(QApplication):
    
    
    def __init__(self, project_path: Path, argv: list[str]=sys.argv) -> None:
        super(StandaloneApp, self).__init__(argv)
        
        self.main_window: StandaloneMainWindow = StandaloneMainWindow(project_path=project_path)
        self.main_window.show()
        
        
def main() -> None:

    init_pinpin()
    
    app: StandaloneApp = StandaloneApp(project_path=Core.current_project_path())
    app.exec_()
