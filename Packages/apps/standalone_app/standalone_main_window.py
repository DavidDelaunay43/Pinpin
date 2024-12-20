from typing import Union
from Packages.ui.new.base_main_window import BaseMainWindow
from Packages.ui.new import widgets
from Packages.utils.core import Core


class StandaloneMainWindow(BaseMainWindow):


    def _create_ui(self) -> None:
        super(StandaloneMainWindow, self)._create_ui()
        widgets.check_release(Core.current_version(), self)
    
    
    def _create_widgets(self) -> None:
        super()._create_widgets()
        self._open_file_widget: widgets.OpenFileWidget = widgets.OpenFileWidget(dev_mode = Core.pref_infos().DEV_MODE, ui_pref_jsonfile = Core.prefs_paths().UI_PREFS_JSONFILE)
        
        
    def _create_layout(self) -> None:
        super()._create_layout()
        self._browser_grid_layout.addWidget(self._open_file_widget, self.LIST01_SIZE[0]+self.TABLE_SIZE[0], self.TREE_SIZE[1], 1, 3)


    def _create_connections(self) -> None:
        super()._create_connections()
        self._table_widget.itemDoubleClicked.connect(self._open_file_widget.open_file)


    def _update_current_path(self, 
                             item: Union[widgets.PipelineWidgetItem, None] = None, 
                             column: Union[int, None] = None
                             ) -> None:
        
        super()._update_current_path(item, column)
        sender = self.sender() if isinstance(self.sender(), widgets.CheckableButton) else item
        self._open_file_widget.update_widget(sender.pipeline_path)
    