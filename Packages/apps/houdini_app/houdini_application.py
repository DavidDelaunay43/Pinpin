from Packages.apps.houdini_app.houdini_main_window import HoudiniMainWindow
from Packages.utils.core import Core
import hou


def main() -> None:

    houdini_app: HoudiniMainWindow = HoudiniMainWindow(
        project_path = Core.current_project_path(),
        parent = hou.ui.mainQtWindow()
    )
