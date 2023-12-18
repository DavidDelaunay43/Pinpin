
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QDialog, QSizePolicy, QLabel, QPushButton, QSpacerItem, QLineEdit, QWidget, QHBoxLayout, QComboBox, QVBoxLayout, QLayout, QColorDialog,QScrollArea
import json
import os

from Packages.utils.funcs import read_json_file, add_text_to_line_edit, set_style_sheet,get_current,change_current,write_json_file
from Packages.utils.constants import CURRENT_STYLE ,STYLE_PATH,PALETTE_PATH,PROJECT_JSON_PATH,ICON_PATH,PROJECT_JSON_PATH,DEV_MODE_JSON,APPS_JSON_PATH


class loadingDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("loading")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(os.path.join(ICON_PATH,"pinpin_icon.ico")))
        self.setObjectName(u"loading_window_container")
        self.resize(430, 550)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(430, 700))
        self.setMaximumSize(QSize(430, 700))
        self.setLayoutDirection(Qt.LeftToRight)
        style_path=os.path.join(STYLE_PATH, CURRENT_STYLE)
        set_style_sheet(self,style_path,PALETTE_PATH)

        self.create_widget()
        self.create_layout()
        self.connect_buttons()

        
    def create_widget(self):
        self.loading_label = QLabel()
        self.loading_label.setObjectName(u"loading_label")
        self.loading_label.setText("loading...")


    def create_layout(self):


        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.option_container_widget = QWidget(self)
        self.option_container_widget.setObjectName(u"option_container")
        self.option_container_layout = QVBoxLayout(self.option_container_widget)
        self.option_container_layout.setObjectName(u"option_container_layout")

        self.option_container_layout.addWidget(self.loading_label)
    
        
        self.verticalLayout.addWidget(self.option_container_widget)

    def connect_buttons(self):
       pass

