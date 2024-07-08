import os
from maya import cmds
from PySide2.QtWidgets import (
    QWidget,
    QDialog,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QRadioButton
)
from Packages.utils.constants.constants_old import CACHE_DIR
from Packages.apps.maya_app.funcs.alembic import (
    get_time_slider_range,
    get_char_sets,
    export_alembics,
    import_alembics,
)
from Packages.apps.maya_app.ui.maya_main_window import maya_main_window
from Packages.apps.maya_app.funcs.get_cameras import find_camera


class AlembicDialog(QDialog):

    def __init__(self, parent=maya_main_window()):
        super(AlembicDialog, self).__init__(parent)
        self.init_ui()
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.show()

    def init_ui(self):
        self.setWindowTitle("Alembic Tools v2")

    def create_widgets(self):

        self.export_radiobtn = QRadioButton("Export")
        self.export_radiobtn.setChecked(True)
        self.import_radiobtn = QRadioButton("Import")

        start, end = get_time_slider_range()

        self.start_lineedit = QLineEdit(str(start))
        self.end_lineedit = QLineEdit(str(end))

        self.cb_char_sets = []

        for camera in find_camera():
            camera = QCheckBox(char_set)
            camera.setChecked(True)
            self.cb_char_sets.append(camera)

        for char_set in get_char_sets():
            cb_char_set = QCheckBox(char_set)
            cb_char_set.setChecked(True)
            self.cb_char_sets.append(cb_char_set)

        self.run_btn = QPushButton("Run")

    def create_layout(self):

        self.main_layout = QVBoxLayout(self)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.main_layout.addWidget(self.grid_widget)

        self.grid_layout.addWidget(self.export_radiobtn, 0, 0)
        self.grid_layout.addWidget(self.import_radiobtn, 0, 1)

        self.grid_layout.addWidget(self.start_lineedit, 1, 0)
        self.grid_layout.addWidget(self.end_lineedit, 1, 1)

        for index, cb_char_set in enumerate(self.cb_char_sets, start=2):
            self.grid_layout.addWidget(cb_char_set, index, 0)

        self.main_layout.addWidget(self.run_btn)

    def create_connections(self):

        self.run_btn.clicked.connect(self.run)

    def run(self):

        scene_name: str = os.path.basename(cmds.file(query=True, sceneName=True))
        _, seq_num, sh_num, _, _, _ = scene_name.split("_")
        directory = os.path.join(CACHE_DIR, seq_num, sh_num)

        char_sets = []
        for cb_char_set in self.cb_char_sets:
            if cb_char_set.isChecked():
                char_sets.append(cb_char_set.text())

        if self.export_radiobtn.isChecked():
            start, end = self.start_lineedit.text(), self.end_lineedit.text()
            export_alembics(start, end, char_sets, directory)
            return

        if self.import_radiobtn.isChecked():
            import_alembics(char_sets, directory)
            return
