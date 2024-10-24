from Packages.apps.maya_app.ui.maya_main_window import MayaMainWindow
from Packages.apps.maya_app.utils.ui_utils import mayaMainWindow
from Packages.utils.core import Core


def main() -> None:

    maya_app: MayaMainWindow = MayaMainWindow(
        project_path = Core.current_project_path(),
        parent = mayaMainWindow()
    )

    maya_app.show()
