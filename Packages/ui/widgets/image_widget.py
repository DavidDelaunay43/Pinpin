import os
import sys
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QDropEvent, QImageReader
from PySide2.QtWidgets import QMenu, QAction, QLabel, QFileDialog
from Packages.utils.constants.constants_old import NO_PREVIEW_FILEPATH, SITE_PACKAGES_PATH
from Packages.utils.constants.project_pinpin_data import pinpin_data_PREVIEW

class ImageWidget(QLabel):
    
    def __init__(self, parent = None, filepath = "", image: bool = False) -> None:
        super(ImageWidget, self).__init__(parent)
    
        if image:
            self._IMAGE_PATH = filepath
            
        else:
            self._FILE_PATH = filepath
            self._FILE_NAME = os.path.basename(filepath)
            self._IMAGE_NAME = f'{self._FILE_NAME}.png'
            self._IMAGE_PATH = os.path.join(pinpin_data_PREVIEW, self._IMAGE_NAME)
        
        self._set_image()
        self.data = {}
        
        self._create_widgets()
        self._create_connections()
        self.setAcceptDrops(True)
        
    def setData(self, role: int, value):
        '''
        '''
        
        self.data[role] = value
        
    def data(self, role: int):
        '''
        '''
        
        return self.data[role]
        
    def _create_widgets(self):
        
        # Créer l'action clic-droit
        self.context_menu = QMenu(self)
        
        self.insert_image_action = QAction('Insert image', self)
        self.insert_image_action.triggered.connect(self.insert_image)
        self.context_menu.addAction(self.insert_image_action)
        
        self.delete_image_action = QAction('Delete image', self)
        self.delete_image_action.triggered.connect(self.delete_image)
        self.context_menu.addAction(self.delete_image_action)
        
    
    def _create_connections(self):
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, event):
        self.context_menu.exec_(self.mapToGlobal(event))
    
    def _set_image(self):
        """
        """
        
        
        if os.path.exists(self._IMAGE_PATH):
            image_path = self._IMAGE_PATH
        
        else:
            image_path = NO_PREVIEW_FILEPATH
            
        self._set_pixmap(image_path)
    
    def delete_image(self):
        os.remove(self._IMAGE_PATH)
        self._set_image()
       
    def insert_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setWindowTitle("Sélectionner une image")
        
        image_filepath, _ = file_dialog.getOpenFileName(self, "Sélectionner une image", "", "Images (*.png *.jpg *.bmp *.gif *.jpeg *.ico)", options=options)
        
        if image_filepath:
            self._IMAGE_PATH = self._save_image(image_filepath, self._FILE_PATH)
            self._set_image()
            
    def _set_pixmap(self, image_filepath):
        
        # Charger l'image sélectionnée dans le QLabel
        pixmap = QPixmap(image_filepath)
        
        # Taille maximale que vous souhaitez définir
        max_width = 180
        max_height = 101
        
        # Redimensionner l'image pour s'adapter à la taille maximale tout en préservant l'aspect
        pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.setPixmap(pixmap)
        self.setText("")
        self.image_path = image_filepath
        
    def _save_image(self, image_path: str, file_path: str, new_size = (180, 101)):
        """
        """
        sys.path.append(SITE_PACKAGES_PATH)
        from PIL import Image
        
        file_name = os.path.basename(file_path)
        
        preview_image_path = os.path.join(pinpin_data_PREVIEW, f'{file_name}.png')
        
        if os.path.exists(preview_image_path):
            os.remove(preview_image_path)
        
        
        if os.path.splitext(image_path)[-1] == ".png":
            image = Image.open(image_path)
            preview_image = image.resize(new_size)
            preview_image.save(preview_image_path)
            
        else:
            image = Image.open(image_path)
            image_png = image.convert('RGBA')
            image_png = image.resize(new_size)
            image_png.save(preview_image_path, "PNG")
        
        return preview_image_path
    
    def dragEnterEvent(self, event: QDropEvent):
        mime_data = event.mimeData()
        if mime_data.hasUrls() and len(mime_data.urls()) == 1:
            url = mime_data.urls()[0]
            if url.isLocalFile() and QImageReader.supportedImageFormats():
                event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        image_url = event.mimeData().urls()[0]
        image_path = image_url.toLocalFile()
        self._save_image(image_path, self._FILE_PATH)
        self._set_image()
