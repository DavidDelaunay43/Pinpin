import hou
from Packages.apps.houdini_app.ui.houdini_main_window import HoudiniMainWindow
from Packages.utils.core import Core
from Packages.utils.init_pinpin import main as init_pinpin


def main() -> None:

    init_pinpin()

    houdini_app: HoudiniMainWindow = HoudiniMainWindow(
        project_path = Core.current_project_path(),
        parent = hou.ui.mainQtWindow()
    )

    houdini_app.show()
