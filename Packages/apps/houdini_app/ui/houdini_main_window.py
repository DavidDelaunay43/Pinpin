from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QPushButton
import hou
from Packages.ui.new.base_main_window import BaseMainWindow
from Packages.utils.core import Core


class HoudiniMainWindow(BaseMainWindow):


    def _create_widgets(self) -> None:
        super(HoudiniMainWindow, self)._create_widgets()
        self._houdini_widget: QPushButton = QPushButton('Open', self)
        self._houdini_widget.setMinimumHeight(50)
        self._houdini_widget.setIcon(
            QIcon(
                str(Core.pinpin_icons_path().joinpath('open_icon.ico'))
            )
        )
        self._houdini_widget.clicked.connect(self._open_file)


    def _create_layout(self) -> None:
        super()._create_layout()
        self._browser_grid_layout.addWidget(self._houdini_widget, self.LIST01_SIZE[0]+self.TABLE_SIZE[0], self.TREE_SIZE[1], 1, 3)


    def _open_file(self) -> None:
        hou.hipFile.load(str(self.current_path).replace('\\', '/'))
