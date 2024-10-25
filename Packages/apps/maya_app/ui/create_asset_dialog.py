from PySide2.QtWidgets import QCheckBox, QComboBox, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton
from Packages.apps.maya_app.utils.create_asset import CreateAsset
from Packages.apps.maya_app.utils.ui_utils import mayaMainWindow


class CreateAssetDialog(QDialog):


    ASSET_TYPES: list[str] = ['01_character', '02_prop', '03_item', '04_enviro', '05_module']
    SUBFOLDERS: list[str] = ['cache', 'clip', 'data', 'images', 'movie', 'out', 'scenes', 'scripts', 'sound', 'sourceimages']
    SF_DEFAULTS: list[int] = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0]
    DEPARTMENTS: list[str] = ['geo', 'grm', 'ldv', 'rig']
    DEP_DEFAULTS: list[int] = [1, 0, 1, 1]


    def __init__(self, parent):
        super(CreateAssetDialog, self).__init__(parent)

        self.setWindowTitle('Create asset')

        self._main_layout: QGridLayout = QGridLayout(self)
        self.setLayout(self._main_layout)


        self.asset_type_label = QLabel('Asset type:', self)
        self._main_layout.addWidget(self.asset_type_label, 0, 0, 1, 1)
        self.asset_type_combo_box: QComboBox = QComboBox(self)
        self.asset_type_combo_box.addItems(self.ASSET_TYPES)
        self._main_layout.addWidget(self.asset_type_combo_box, 0, 1, 1, 1)

        self.asset_name_label = QLabel('Asset name:', self)
        self._main_layout.addWidget(self.asset_name_label, 1, 0, 1, 1)
        self.asset_name_line_edit = QLineEdit('', self)
        self._main_layout.addWidget(self.asset_name_line_edit, 1, 1, 1, 1)

        self._maya_project_label: QLabel = QLabel('Project name:', self)
        self._main_layout.addWidget(self._maya_project_label, 2, 0, 1, 1)
        self._maya_project_line_edit: QLineEdit = QLineEdit('maya', self)
        self._main_layout.addWidget(self._maya_project_line_edit, 2, 1, 1, 1)

        self._subfolders_label: QLabel = QLabel('Subfolders:', self)
        self._main_layout.addWidget(self._subfolders_label, 3, 0, 1, 1)
        self._subfolder_checkboxes: list[QCheckBox] = []
        for index, (subfolder, sf_default) in enumerate(zip(self.SUBFOLDERS, self.SF_DEFAULTS)):
            check_box: QCheckBox = QCheckBox(subfolder, self)
            check_box.setChecked(sf_default)
            self._main_layout.addWidget(check_box, index+3, 1, 1, 2)
            self._subfolder_checkboxes.append(check_box)

        self._department_label: QLabel = QLabel('Departments:', self)
        self._main_layout.addWidget(self._department_label, len(self.SUBFOLDERS)+3, 0, 1, 1)
        self._deparments_checkboxes: list[QCheckBox] = []
        for index, (department, dep_default) in enumerate(zip(self.DEPARTMENTS, self.DEP_DEFAULTS)):
            check_box: QCheckBox = QCheckBox(department, self)
            check_box.setChecked(dep_default)
            self._main_layout.addWidget(check_box, index+len(self.SUBFOLDERS)+3, 1, 1, 1)
            self._deparments_checkboxes.append(check_box)

        self._run_button: QPushButton = QPushButton('Create Asset', self)
        self._run_button.clicked.connect(self.accept)
        self._run_button.setDefault(True)
        self._main_layout.addWidget(self._run_button, len(self.SUBFOLDERS)+len(self.DEPARTMENTS)+3, 0, 1, 2)


    @property
    def asset_name(self) -> str:
        return self.asset_name_line_edit.text()
    

    @property
    def asset_type(self) -> str:
        return self.asset_type_combo_box.currentText()
    

    @property
    def project_name(self) -> str:
        return self._maya_project_line_edit.text()
    

    @property
    def subfolders(self) -> list[str]:
        return [sf_cb.text() for sf_cb in self._subfolder_checkboxes if sf_cb.isChecked()]
    

    @property
    def departments(self) -> list[str]:
        return [dep_cb.text() for dep_cb in self._deparments_checkboxes if dep_cb.isChecked()]
    

    def accept(self) -> None:
        asset: CreateAsset = CreateAsset(
            self.asset_name,
            self.asset_type,
            self.project_name,
            self.subfolders,
            self.departments
        )
        asset.create()
        super(CreateAssetDialog, self).accept()


def main() -> None:
    create_asset_dialog: CreateAssetDialog = CreateAssetDialog(mayaMainWindow())
    create_asset_dialog.exec_()
