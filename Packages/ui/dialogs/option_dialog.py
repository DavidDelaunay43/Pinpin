import os
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QDialog, QSizePolicy, QLabel, QPushButton, QSpacerItem, QLineEdit, 
                               QWidget, QHBoxLayout, QComboBox, QVBoxLayout, QLayout, QCheckBox,
                               QColorDialog,QScrollArea,QTabWidget, QGridLayout)
from Packages.utils.funcs import read_json_file, add_text_to_line_edit, set_style_sheet, write_json_file
from Packages.utils.constants.preferences import UI_PREFS_JSON_PATH, APPS_JSON_PATH
from Packages.utils.constants.project_files import CURRENT_STYLE, STYLE_PATH, PALETTE_PATH, ICON_PATH
from Packages.utils.logger import init_logger

logger = init_logger(__file__)

class OptionDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(os.path.join(ICON_PATH,"pinpin_icon.ico")))
        self.setObjectName(u"option_window_container")
        self.resize(430, 550)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(430, 700))
        #self.setMaximumSize(QSize(430, 700))
        self.setLayoutDirection(Qt.LeftToRight)
        style_path=os.path.join(STYLE_PATH, CURRENT_STYLE)
        set_style_sheet(self,style_path,PALETTE_PATH)

        self.create_widget()
        self.create_layout()
        self.connect_buttons()
        self.update_line_edit()

        
    def create_widget(self):
        self.restart_label = QLabel()
        self.restart_label.setObjectName(u"restart_label")
        self.restart_label.setText("↓ restart pinpin to see any changement about the below settings ↓")

        self.apply_button = QPushButton()
        self.apply_button.setObjectName(u"apply_button")
        self.apply_button.setMinimumSize(QSize(0, 40))
        self.apply_button.setText("apply")

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        def create_variable_row(row_name,type):
            margin=2

            label = QLabel()
            label.setObjectName(row_name+"_label")
            if type=="pref":
                label.setText(row_name+"_path")
            if type=="color":
                label.setText(row_name)
            
            line_edit = QLineEdit()
            line_edit.setObjectName(row_name+"_line_edit")
            line_edit.setMaximumSize(QSize(1000, 30))
            line_edit.setMinimumSize(QSize(10, 30))

            layout_widget = QWidget()
            layout_widget.setObjectName(row_name+"_widget_layout")
            layout = QHBoxLayout(layout_widget)
            layout.setContentsMargins(margin, margin, margin, margin)
            layout.setObjectName(row_name+"_layout")
            layout.addWidget(label)
            layout.addWidget(line_edit)

            if type=="color":
                button=QPushButton()
                button.setObjectName(row_name+"_button")
                button.setMaximumSize(QSize(40, 40))
                button.setMinimumSize(QSize(40, 40))
                
                color_icon=os.path.join(ICON_PATH, "color.png")
                button.setIcon(QIcon(color_icon))
                layout.addWidget(button)

            
            if type=="pref":
                
                label_pref = QLabel()
                label_pref.setObjectName(row_name+"_pref_label")
                label_pref.setText(row_name+"_pref")

                line_edit_pref = QLineEdit()
                line_edit_pref.setObjectName(row_name+"_pref_line_edit")
                line_edit_pref.setMaximumSize(QSize(1000, 30))
                line_edit_pref.setMinimumSize(QSize(10, 30))

                layout_pref_widget = QWidget()
                layout_pref = QHBoxLayout(layout_pref_widget)
                layout_pref.setContentsMargins(margin, margin, margin, margin)
                layout_pref.setObjectName(row_name+"_layout_pref")
                layout_pref.addWidget(label_pref)
                layout_pref.addWidget(line_edit_pref)

                layout_main_pref_widget=QWidget()
                layout_main_pref_widget.setObjectName(row_name+"_layout_main_pref_widget")
                main_layout_pref = QVBoxLayout(layout_main_pref_widget)
                main_layout_pref.setSpacing(1)
                main_layout_pref.addWidget(layout_widget)
                main_layout_pref.addWidget(layout_pref_widget)
                



            if type=="color":
                return layout_widget,button,line_edit
            if type=="pref":
                return layout_main_pref_widget,line_edit,line_edit_pref


        def create_project_row():
            label = QLabel()
            label.setObjectName("project_label")
            label.setText("project :")

            self.project_combo_box = QComboBox()
            self.project_combo_box.setMaximumSize(QSize(1000, 30))
            self.project_combo_box.setMinimumSize(QSize(10, 30))

            project_layout_widget = QWidget()
            project_layout_widget.setObjectName("project_layout_widget")
            project_layout = QHBoxLayout(project_layout_widget)
            project_layout.setObjectName("project_row_layout")
            project_layout.addWidget(label)
            project_layout.addWidget(self.project_combo_box)

            self.fill_project_combobox(self.project_combo_box)
            return project_layout_widget
    

        def create_dev_mode_row():
            self.dev_mode_button = QPushButton()
            self.dev_mode_button.setObjectName("dev_mode_button")
            self.dev_mode_button.setText("dev mode")
            self.dev_mode_button.setCheckable(True)
            self.dev_mode_button.setMaximumSize(QSize(1000, 30))
            self.dev_mode_button.setMinimumSize(QSize(10, 30))
    
            dev_mode_state=self.get_dev_mode_state()
            if dev_mode_state == 1:
                self.dev_mode_button.setChecked(True)
            else :
                self.dev_mode_button.setChecked(False)

            dev_mode_layout_widget = QWidget()
            dev_mode_layout_widget.setObjectName("dev_mode_layout_widget")
            dev_mode_project_layout = QHBoxLayout(dev_mode_layout_widget)
            dev_mode_project_layout.setObjectName("dev_mode_project_layout")
            dev_mode_project_layout.addWidget(self.dev_mode_button)

            return dev_mode_layout_widget
        
        def create_special_ui_row():
            self.special_ui_button = QPushButton()
            self.special_ui_button.setObjectName("special_ui_button")
            self.special_ui_button.setText("special ui :]")
            self.special_ui_button.setCheckable(True)
            self.special_ui_button.setMaximumSize(QSize(1000, 30))
            self.special_ui_button.setMinimumSize(QSize(10, 30))
   
            special_ui_state=self.get_special_ui_state()
            if special_ui_state == 1:
                self.special_ui_button.setChecked(True)
            else :
                self.special_ui_button.setChecked(False)


            special_ui_layout_widget = QWidget()
            special_ui_layout_widget.setObjectName("special_ui_layout_widget")
            special_ui_layout = QHBoxLayout(special_ui_layout_widget)
            special_ui_layout.setObjectName("special_ui_layout")
            special_ui_layout.addWidget(self.special_ui_button)


            return special_ui_layout_widget

        def create_theme_row():

            self.themes_layout_widget = QWidget()
            self.themes_layout_widget.setObjectName("themes_layout_widget")
            self.themes_layout = QHBoxLayout(self.themes_layout_widget)
            self.themes_layout.setObjectName("themes_layout")

            def create_theme_button(theme_name):
                button=QPushButton()
                button.setObjectName(theme_name+"_button")
                button.setMaximumSize(QSize(100000, 40))
                button.setMinimumSize(QSize(0, 40))
                button.setText(theme_name)
                self.themes_layout.addWidget(button)
                return button

            self.dark_theme_button=create_theme_button("dark")
            self.light_theme_button=create_theme_button("light")

            

            return self.themes_layout_widget
        

        self.main_color_row,self.main_color_button,self.main_color_line_edit=create_variable_row("main_color","color")
        self.secondary_color_row,self.secondary_color_button,self.secondary_color_line_edit=create_variable_row("secondary_color","color")
        self.terteary_color_row,self.terteary_color_button,self.terteary_color_line_edit=create_variable_row("terteary_color","color")
        self.color_4_row,self.color_4_button,self.color_4_line_edit=create_variable_row("color_4","color")
        self.cute_color_row,self.cute_color_button,self.cute_color_line_edit=create_variable_row("cute_color","color")
        self.theme_row=create_theme_row()
        self.project_row=create_project_row()
        self.dev_mode_row=create_dev_mode_row()
        self.special_ui_row=create_special_ui_row()

        self.maya_pref_row,self.maya_path_line_edit,self.maya_pref_line_edit=create_variable_row("maya","pref")
        self.houdini_pref_row,self.houdini_path_line_edit,self.houdini_pref_line_edit=create_variable_row("houdini","pref")
        self.blender_pref_row,self.blender_path_line_edit,self.blender_pref_line_edit=create_variable_row("blender","pref")
        self.krita_pref_row,self.krita_path_line_edit,self.krita_pref_line_edit=create_variable_row("krita","pref")
        self.nuke_pref_row,self.nuke_path_line_edit,self.nuke_pref_line_edit=create_variable_row("nuke","pref")
        self.photoshop_pref_row,self.photoshop_path_line_edit,self.photoshop_pref_line_edit=create_variable_row("photoshop","pref")
        self.resolve_pref_row,self.resolve_path_line_edit,self.resolve_pref_line_edit=create_variable_row("resolve","pref")
        self.zbrush_pref_row,self.zbrush_path_line_edit,self.zbrush_pref_line_edit=create_variable_row("zbrush","pref")

        #☻ ui tab widget -------------------------------------------------
        self.num_files_label = QLabel('Num files')
        self.num_files_line_edit = QLineEdit('')
        self.sort_files_cb = QCheckBox('Reverse sort files')
        self.update_ui_widget()

    def create_layout(self):

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)

        self._tab_widget = QTabWidget()
        
        self.verticalLayout.addWidget(self._tab_widget)

         # ui tab --------------------------------------------------------------------------------------------------------
        self.ui_tab_layout_widget = QWidget()
        self.ui_tab_layout = QVBoxLayout()
        self.ui_tab_layout_widget.setLayout(self.ui_tab_layout)
        self._tab_widget.addTab( self.ui_tab_layout_widget, 'ui')

        self.ui_grid_widget = QWidget()
        self.ui_grid_layout = QGridLayout()
        self.ui_grid_widget.setLayout(self.ui_grid_layout)
        self.ui_tab_layout.addWidget(self.ui_grid_widget)
        self.ui_grid_layout.setAlignment(Qt.AlignTop)

        self.ui_grid_layout.addWidget(self.num_files_label, 0, 0)
        self.ui_grid_layout.addWidget(self.num_files_line_edit, 0, 1)
        self.ui_grid_layout.addWidget(self.sort_files_cb, 1, 0)

        #customize_tab--------------------------------------------------------------------------------
        self.customize_tab_layout_widget = QWidget()
        self.customize_tab_layout_widget.setObjectName("customize_tab_layout_widget")
        self.customize_tab_layout = QVBoxLayout()
        self.customize_tab_layout_widget.setLayout(self.customize_tab_layout)
        self._tab_widget.addTab(self.customize_tab_layout_widget, 'customize')

        self.customize_tab_scroll_area = QScrollArea()
        self.customize_tab_scroll_area.setWidgetResizable(True)
        
        self.customize_tab_scroll_area_layout_widget = QWidget(self)
        self.customize_tab_scroll_area_layout = QVBoxLayout(self.customize_tab_scroll_area_layout_widget)
        self.customize_tab_scroll_area.setWidget(self.customize_tab_scroll_area_layout_widget)

        self.customize_tab_layout.addWidget(self.customize_tab_scroll_area)

        self.customize_tab_scroll_area_layout.addWidget(self.cute_color_row)
        self.customize_tab_scroll_area_layout.addWidget(self.main_color_row)
        self.customize_tab_scroll_area_layout.addWidget(self.secondary_color_row)
        self.customize_tab_scroll_area_layout.addWidget(self.terteary_color_row)
        self.customize_tab_scroll_area_layout.addWidget(self.color_4_row)
        self.customize_tab_scroll_area_layout.addWidget(self.theme_row)

        self.customize_tab_verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.customize_tab_scroll_area_layout.addItem(self.customize_tab_verticalSpacer)


        #preferences_folders_tab--------------------------------------------------------------------------
        self.preferences_folders_tab_layout_widget = QWidget()
        self.preferences_folders_tab_layout = QVBoxLayout()
        self.preferences_folders_tab_layout_widget.setLayout(self.preferences_folders_tab_layout)
        self._tab_widget.addTab( self.preferences_folders_tab_layout_widget, 'preferences_folders')

        self.preferences_folders_tab_scroll_area = QScrollArea()
        self.preferences_folders_tab_scroll_area.setWidgetResizable(True)
        self.preferences_folders_tab_scroll_area_layout_widget = QWidget(self)
        self.preferences_folders_tab_scroll_area_layout = QVBoxLayout(self.preferences_folders_tab_scroll_area_layout_widget)
        self.preferences_folders_tab_scroll_area.setWidget(self.preferences_folders_tab_scroll_area_layout_widget)

        self.preferences_folders_tab_layout.addWidget(self.preferences_folders_tab_scroll_area)

        self.preferences_folders_tab_scroll_area_layout.addWidget(self.maya_pref_row)
        self.preferences_folders_tab_scroll_area_layout.addWidget(self.houdini_pref_row)
        self.preferences_folders_tab_scroll_area_layout.addWidget(self.blender_pref_row)
        self.preferences_folders_tab_scroll_area_layout.addWidget(self.krita_pref_row)
        self.preferences_folders_tab_scroll_area_layout.addWidget(self.nuke_pref_row)
        self.preferences_folders_tab_scroll_area_layout.addWidget(self.photoshop_pref_row)
        self.preferences_folders_tab_scroll_area_layout.addWidget(self.resolve_pref_row)
        self.preferences_folders_tab_scroll_area_layout.addWidget(self.zbrush_pref_row)

        self.preferences_folders_tab_verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.preferences_folders_tab_scroll_area_layout.addItem(self.preferences_folders_tab_verticalSpacer)

        #other_tab----------------------------------------------------------------------------------------
        self.other_tab_layout_widget = QWidget()
        self.other_tab_layout = QVBoxLayout()
        self.other_tab_layout_widget.setLayout(self.other_tab_layout)
        self._tab_widget.addTab( self.other_tab_layout_widget, 'other')

        self.other_tab_scroll_area = QScrollArea()
        self.other_tab_scroll_area.setWidgetResizable(True)
        self.other_tab_scroll_area_layout_widget = QWidget(self)
        self.other_tab_scroll_area_layout = QVBoxLayout(self.other_tab_scroll_area_layout_widget)
        self.other_tab_scroll_area.setWidget(self.other_tab_scroll_area_layout_widget)

        self.other_tab_layout.addWidget(self.other_tab_scroll_area)

        self.other_tab_scroll_area_layout.addWidget(self.restart_label)
        self.other_tab_scroll_area_layout.addWidget(self.project_row)
        self.other_tab_scroll_area_layout.addWidget(self.dev_mode_row)
        self.other_tab_scroll_area_layout.addWidget(self.special_ui_row)

        self.other_tab_verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.other_tab_scroll_area_layout.addItem(self.other_tab_verticalSpacer)

    def connect_buttons(self):

        self.main_color_button.clicked.connect(self.showColorDialog)
        self.secondary_color_button.clicked.connect(self.showColorDialog)
        self.terteary_color_button.clicked.connect(self.showColorDialog)
        self.cute_color_button.clicked.connect(self.showColorDialog)
        self.color_4_button.clicked.connect(self.showColorDialog)
        self.dark_theme_button.clicked.connect(self.set_theme)
        self.light_theme_button.clicked.connect(self.set_theme)
        self.dev_mode_button.clicked.connect(self.change_dev_mode_state)
        self.special_ui_button.clicked.connect(self.change_ui_special_state)
        self.project_combo_box.currentIndexChanged.connect(self.update_current_project)

        self.blender_path_line_edit.textChanged.connect(self.write_apps)
        self.blender_pref_line_edit.textChanged.connect(self.write_apps)

        self.maya_path_line_edit.textChanged.connect(self.write_apps)
        self.maya_pref_line_edit.textChanged.connect(self.write_apps)

        self.krita_path_line_edit.textChanged.connect(self.write_apps)
        self.krita_pref_line_edit.textChanged.connect(self.write_apps)

        self.resolve_path_line_edit.textChanged.connect(self.write_apps)
        self.resolve_pref_line_edit.textChanged.connect(self.write_apps)

        self.photoshop_path_line_edit.textChanged.connect(self.write_apps)
        self.photoshop_pref_line_edit.textChanged.connect(self.write_apps)

        self.nuke_path_line_edit.textChanged.connect(self.write_apps)
        self.nuke_pref_line_edit.textChanged.connect(self.write_apps)

        self.zbrush_path_line_edit.textChanged.connect(self.write_apps)
        self.zbrush_pref_line_edit.textChanged.connect(self.write_apps)

        self.sort_files_cb.stateChanged.connect(self.update_ui_pref)
        self.num_files_line_edit.textChanged.connect(self.update_ui_pref)

    def update_ui_pref(self):

        from Packages.logic.json_funcs import json_to_dict, dict_to_json

        if self.sender() == self.sort_files_cb:

            dico = json_to_dict(UI_PREFS_JSON_PATH)
            dico['reverse_sort_file'] = self.sort_files_cb.isChecked()
            dict_to_json(dico, UI_PREFS_JSON_PATH)

        elif self.sender() == self.num_files_line_edit:

            dico = json_to_dict(UI_PREFS_JSON_PATH)
            try:
                dico['num_files'] = int(self.num_files_line_edit.text())
            except:
                dico['num_files'] = self.num_files_line_edit.text()
            dict_to_json(dico, UI_PREFS_JSON_PATH)

        else:
            pass

        self.update_ui_widget()
        
    def update_ui_widget(self):
        from Packages.logic.json_funcs import json_to_dict

        reverse_sort = json_to_dict(UI_PREFS_JSON_PATH)['reverse_sort_file']
        self.sort_files_cb.setChecked(reverse_sort)

        num_files = json_to_dict(UI_PREFS_JSON_PATH)['num_files']
        self.num_files_line_edit.setText(str(num_files))

    def fill_project_combobox(self,combo_box):
        pass
        """with open(PROJECT_JSON_PATH, 'r') as file:
            project_json = json.load(file)

        projects = project_json["projects"]
        current_project = list(project_json["current_project"].keys())[0]
        
        for i in projects.keys():
            combo_box.addItem(i)

        combo_box.setCurrentText(current_project)"""

#UTILS
    def showColorDialog(self):
        
        color_dialog = QColorDialog()
        color = color_dialog.getColor()
        sender = self.sender()
        print(sender)
        
        if sender == self.main_color_button:
            line_edit=self.main_color_line_edit
        if sender == self.secondary_color_button:
            line_edit=self.secondary_color_line_edit
        if sender == self.terteary_color_button:
            line_edit=self.terteary_color_line_edit
        if sender == self.cute_color_button:
            line_edit=self.cute_color_line_edit
        if sender == self.color_4_button:
            line_edit=self.color_4_line_edit

        line_edit.setText(color.name())

        self.refresh_style()

    def set_theme(self):
        sender = self.sender()

        if sender == self.dark_theme_button:
            main_color="#262626"
            secondary_color="#0d0d0d"
            terteary_color="#C2C2C2"
            color_4="#1a1a1a"
            cute_color="#d1a024"
        if sender == self.light_theme_button:
            main_color="#cacaca"
            secondary_color="#ebebeb"
            terteary_color="#000000"
            color_4="#c5c5c5"
            cute_color="#00ffff"
            

        self.main_color_line_edit.setText(main_color)
        self.secondary_color_line_edit.setText(secondary_color)
        self.terteary_color_line_edit.setText(terteary_color)
        self.cute_color_line_edit.setText(cute_color)
        self.color_4_line_edit.setText(color_4)

        self.refresh_style()

    def write_palette(self):

        write_json_file(PALETTE_PATH,"MAIN_COLOR",self.main_color_line_edit.text())
        write_json_file(PALETTE_PATH,"SECONDARY_COLOR",self.secondary_color_line_edit.text())
        write_json_file(PALETTE_PATH,"TERTEARY_COLOR",self.terteary_color_line_edit.text())
        write_json_file(PALETTE_PATH,"CUTE_COLOR",self.cute_color_line_edit.text())
        write_json_file(PALETTE_PATH,"COLOR_4",self.color_4_line_edit.text())
        
    def change_ui_special_state(self):
        pass
        """with open(SPECIAL_UI_JSON, 'r') as file:
            special_ui_data = json.load(file)
        old_special_ui=self.get_special_ui_state()

        if old_special_ui == 0:
            print("activaing special ui")
            
            special_ui_data["special_ui"]=1
        else :
            print("desactivating special ui")
            special_ui_data["special_ui"]=0
       
        with open(SPECIAL_UI_JSON, 'w') as file:
            json.dump(special_ui_data, file, indent=4)
        new_special_ui=self.get_special_ui_state()

        if new_special_ui == 0:
            logger.info("special ui is disabled.")
        else :
            logger.info("special ui is enabled.")"""
            
    def get_special_ui_state(self):
        pass
        """with open(SPECIAL_UI_JSON, 'r') as file:
            special_ui_data = json.load(file)
        special_ui=special_ui_data["special_ui"]
        return special_ui"""

    def write_apps(self):

        write_json_file(APPS_JSON_PATH, "blender", {"path": self.blender_path_line_edit.text(), "pref": self.blender_pref_line_edit.text()})
        write_json_file(APPS_JSON_PATH, "maya", {"path": self.maya_path_line_edit.text(), "pref": self.maya_pref_line_edit.text()})
        write_json_file(APPS_JSON_PATH, "nuke", {"path": self.nuke_path_line_edit.text(), "pref": self.nuke_pref_line_edit.text()})
        write_json_file(APPS_JSON_PATH, "resolve", {"path": self.resolve_path_line_edit.text(), "pref": self.resolve_pref_line_edit.text()})
        write_json_file(APPS_JSON_PATH, "krita", {"path": self.krita_path_line_edit.text(), "pref": self.krita_pref_line_edit.text()})
        write_json_file(APPS_JSON_PATH, "photoshop", {"path": self.photoshop_path_line_edit.text(), "pref": self.photoshop_pref_line_edit.text()})
        write_json_file(APPS_JSON_PATH, "houdini", {"path": self.houdini_path_line_edit.text(), "pref": self.houdini_pref_line_edit.text()})
        write_json_file(APPS_JSON_PATH, "zbrush", {"path": self.zbrush_path_line_edit.text(), "pref": self.zbrush_pref_line_edit.text()})

    def refresh_style(self):
        self.write_palette()
        style_path=os.path.join(STYLE_PATH, CURRENT_STYLE)
        set_style_sheet(self,style_path,PALETTE_PATH)
        print(self.parent())
        papa=self.parentWidget().parentWidget()
        set_style_sheet(papa,style_path,PALETTE_PATH)

    def change_current_project(self,current_project):
        pass
        """old_current_project=get_current_value(PROJECT_JSON_PATH,"current_project")
        old_current_project=list(old_current_project.keys())[0]
        print(old_current_project)
        change_current(PROJECT_JSON_PATH,"current_project","projects",current_project)
        new_current_project=get_current_value(PROJECT_JSON_PATH,"current_project")
        new_current_project=list(new_current_project.keys())[0]

        print("change from the project",old_current_project,"to",new_current_project)"""

    def update_current_project(self):
        self.change_current_project(self.project_combo_box.currentText())
    
    def change_dev_mode_state(self):
        pass
        """with open(DEV_MODE_JSON, 'r') as file:
            dev_mode_data = json.load(file)

        old_dev_mode=self.get_dev_mode_state()

        if old_dev_mode == 0:
            print("activaing dev mode")
            dev_mode_data["dev_mode"]=1
        else :
            print("desactivating dev mode")
            dev_mode_data["dev_mode"]=0
        
        with open(DEV_MODE_JSON, 'w') as file:
            json.dump(dev_mode_data, file, indent=4)
        
        

        new_dev_mode=self.get_dev_mode_state()

        if new_dev_mode == 0:
            print("dev mode is desactivate")
        else :
            print("dev mode is activate")"""
        
    def get_dev_mode_state(self):
        pass
        """with open(DEV_MODE_JSON, 'r') as file:
            dev_mode_data = json.load(file)

        dev_mode=dev_mode_data["dev_mode"]

        return dev_mode"""

    def update_line_edit(self):
        palette = read_json_file(PALETTE_PATH)

        add_text_to_line_edit(self.main_color_line_edit,palette["MAIN_COLOR"])
        add_text_to_line_edit(self.secondary_color_line_edit,palette["SECONDARY_COLOR"])
        add_text_to_line_edit(self.cute_color_line_edit,palette["CUTE_COLOR"])
        add_text_to_line_edit(self.terteary_color_line_edit,palette["TERTEARY_COLOR"])
        add_text_to_line_edit(self.color_4_line_edit,palette["COLOR_4"])

        pref=read_json_file(APPS_JSON_PATH)
        add_text_to_line_edit(self.maya_path_line_edit,pref["maya"]["path"])
        add_text_to_line_edit(self.maya_pref_line_edit,pref["maya"]["pref"])
        add_text_to_line_edit(self.houdini_path_line_edit,pref["houdini"]["path"])
        add_text_to_line_edit(self.houdini_pref_line_edit,pref["houdini"]["pref"])
        add_text_to_line_edit(self.blender_path_line_edit,pref["blender"]["path"])
        add_text_to_line_edit(self.houdini_pref_line_edit,pref["blender"]["pref"])
        add_text_to_line_edit(self.krita_path_line_edit,pref["krita"]["path"])
        add_text_to_line_edit(self.krita_pref_line_edit,pref["krita"]["pref"])
        add_text_to_line_edit(self.nuke_path_line_edit,pref["nuke"]["path"])
        add_text_to_line_edit(self.nuke_pref_line_edit,pref["nuke"]["pref"])
        add_text_to_line_edit(self.photoshop_path_line_edit,pref["photoshop"]["path"])
        add_text_to_line_edit(self.photoshop_pref_line_edit,pref["photoshop"]["pref"])
        add_text_to_line_edit(self.resolve_path_line_edit,pref["resolve"]["path"])
        add_text_to_line_edit(self.resolve_pref_line_edit,pref["resolve"]["pref"])
        add_text_to_line_edit(self.zbrush_path_line_edit,pref["zbrush"]["path"])
        add_text_to_line_edit(self.zbrush_pref_line_edit,pref["zbrush"]["pref"])

