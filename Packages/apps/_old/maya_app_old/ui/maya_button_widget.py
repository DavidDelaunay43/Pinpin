from PySide2.QtWidgets import QWidget, QRadioButton, QVBoxLayout, QHBoxLayout, QLineEdit
from Packages.apps.maya_app_old.ui.maya_button import MayaButton
from Packages.utils.logger import init_logger

logger = init_logger(__file__)

class MayaButtonWidget(QWidget):
    '''
    '''

    def __init__(self, parent = None) -> None:
        super(MayaButtonWidget, self).__init__(parent)
        
        self.mode = 'Open'

        self._create_widgets()
        self._create_layout()
        self._create_connections()

    def _create_widgets(self):

        self._radio_btn_widget = QWidget(self)
        self._open_radio_btn = QRadioButton('Open')
        self._import_radio_btn = QRadioButton('Import')
        self._reference_radio_btn = QRadioButton('Reference')

        self._radio_btn_namespace_widget = QWidget(self)
        self._file_namespace_radio_btn = QRadioButton('file namespace')
        self._custom_namespace_radio_btn = QRadioButton('custom namespace')
        self._no_namespace_radio_btn = QRadioButton('no namespace')
        self._field_custom_namspace = QLineEdit()

        self._open_radio_btn.setChecked(True)
        self._no_namespace_radio_btn.setChecked(True)

        self._file_namespace_radio_btn.setVisible(False)
        self._custom_namespace_radio_btn.setVisible(False)
        self._no_namespace_radio_btn.setVisible(False)
        self._field_custom_namspace.setVisible(False)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        self.maya_button = MayaButton(None, mode = 'open')

    def _create_layout(self):
        
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)

        self._radio_btn_layout = QHBoxLayout()
        self._radio_btn_widget.setLayout(self._radio_btn_layout)

        self._radio_btn_namespace_layout = QHBoxLayout()
        self._radio_btn_namespace_widget.setLayout(self._radio_btn_namespace_layout)

        self._radio_btn_layout.addWidget(self._open_radio_btn)
        self._radio_btn_layout.addWidget(self._import_radio_btn)
        self._radio_btn_layout.addWidget(self._reference_radio_btn)

        self._radio_btn_namespace_layout.addWidget(self._file_namespace_radio_btn)
        self._radio_btn_namespace_layout.addWidget(self._no_namespace_radio_btn)
        self._radio_btn_namespace_layout.addWidget(self._custom_namespace_radio_btn)
        self._radio_btn_namespace_layout.addWidget(self._field_custom_namspace)

        self._main_layout.addWidget(self._radio_btn_widget)
        self._main_layout.addWidget(self._radio_btn_namespace_widget)
        self._main_layout.addWidget(self.maya_button)

    def _create_connections(self):
        
        self._open_radio_btn.clicked.connect(self._toggle_mode)
        self._import_radio_btn.clicked.connect(self._toggle_mode)
        self._reference_radio_btn.clicked.connect(self._toggle_mode)

        self._file_namespace_radio_btn.clicked.connect(self._toggle_mode)
        self._custom_namespace_radio_btn.clicked.connect(self._toggle_mode)
        self._no_namespace_radio_btn.clicked.connect(self._toggle_mode)

    def _toggle_mode(self):
        
        text = self.sender().text()
        if text != 'Open':
            if text in ['Reference', 'Import']:
                for btn in [self._file_namespace_radio_btn, self._custom_namespace_radio_btn, self._no_namespace_radio_btn]:
                    if btn.isChecked():
                        text = f'{text} {btn.text()}'
            else:
                for btn in [self._import_radio_btn, self._reference_radio_btn]:
                    if btn.isChecked():
                        text = f'{btn.text()} {text}'

        self.maya_button.set_mode(text.lower())
        logger.info(f'Get file mode set : {text.lower()}')

        if text == 'Open':
            self._file_namespace_radio_btn.setVisible(False)
            self._custom_namespace_radio_btn.setVisible(False)
            self._no_namespace_radio_btn.setVisible(False)
            self._field_custom_namspace.setVisible(False)

        else:
            self._file_namespace_radio_btn.setVisible(True)
            self._custom_namespace_radio_btn.setVisible(True)
            self._no_namespace_radio_btn.setVisible(True)
            self._field_custom_namspace.setVisible(True)
