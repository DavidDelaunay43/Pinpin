from typing import Union
from Packages.ui.new.widgets.protocols import PipelineWidgetItem
from Packages.apps.maya_app.ui.maya_file_widget import MayaFileWidget
from Packages.ui.new.base_main_window import BaseMainWindow
from Packages.ui.new import widgets


class MayaMainWindow(BaseMainWindow):
    

    def _create_widgets(self) -> None:
        super()._create_widgets()
        self._maya_file_widget: MayaFileWidget = MayaFileWidget(self)


    def _create_layout(self) -> None:
        super(MayaMainWindow, self)._create_layout()
        self._browser_grid_layout.addWidget(self._maya_file_widget, self.LIST01_SIZE[0]+self.TABLE_SIZE[0], self.TREE_SIZE[1], 1, 3)


    def _update_current_path(self, 
                             item: Union[PipelineWidgetItem, None] = None, 
                             column: Union[int, None] = None
                             ) -> None:
        super(MayaMainWindow, self)._update_current_path(item, column)
        sender = self.sender() if isinstance(self.sender(), widgets.CheckableButton) else item
        self._maya_file_widget.update_widget(sender.pipeline_path)
