import json
import os
import subprocess

from Packages.logic.json_funcs import set_recent_file, get_pref
from Packages.utils.constants.preferences import APPS_JSON_PATH
from Packages.utils.constants.pinpin import PINPIN_PATH
from Packages.utils.logger import init_logger
from Packages.logic.open_in_usdview import open_in_usd_view

EXTS = {
    ".abc": "fbxreview",
    ".blend": "blender",
    ".fbx": "fbxreview",
    ".kra": "krita",
    ".hip": "houdini",
    ".hipnc": "houdini",
    ".ma": "maya",
    ".mb": "maya",
    ".nk": "nuke",
    ".obj": "fbxreview",
    ".psd": "photoshop",
    ".drp": "resolve",
    ".uasset": "unreal",
    ".zpr": "zbrush",
    ".ztl": "zbrush",
    ".spp": "substance_painter",
    ".sbs": "substance_designer",
    ".sbsar": "substance_designer",
    ".png": "it",
    ".exr": "it",
    ".tex": "it",
    ".usd": "usdview",
    ".usda": "usdview"
}

logger = init_logger(__file__)

class FileOpener:

    def __init__(self, file_path, pref_path = None):

        self.open_file_in_app(file_path, pref_path)

    def get_file_extension(self, file_path: str) -> str:
        """
        Obtient l'extension d'un fichier à partir de son chemin complet.

        Args:
            file_path (str): Le chemin complet du fichier.

        Returns:
            str: L'extension du fichier (avec le point inclus). Si aucune extension n'est trouvée, une chaîne vide est retournée.
        """
        
        print(f'FILE PATH : {file_path}')
        file_name = os.path.basename(file_path)
        print(f'FILE NAME : {file_name}')
        return os.path.splitext(file_name)[1]

    def get_application(self, extension: str) -> str:
        """
        Obtient l'application associée à une extension de fichier donnée.

        Args:
            extension (str): L'extension du fichier (avec le point inclus).

        Returns:
            str: Le nom de l'application associée à l'extension donnée, ou None si aucune correspondance n'est trouvée.
        """

        if extension in EXTS:
            return EXTS[extension]

    def get_application_path(self, application: str) -> str:
        """
        Obtient le chemin d'exécution de l'application donnée.

        Args:
            application (str): Le nom de l'application.

        Returns:
            str: Le chemin d'exécution de l'application, ou None si l'application n'est pas trouvée.
        """

        with open(APPS_JSON_PATH, 'r') as file:
            APPS = json.load(file)
        
        if application in APPS:
            return APPS[application]["path"]

    def open_file_in_app(self, file_path: str, pref_path = None):
        """
        Ouvre un fichier dans l'application associée à son extension.

        Args:
            file_path (str): Chemin d'accès complet au fichier.

        Returns:
            None
        """
        
        pref_dict = {
            'houdini': 'HOUDINI_USER_PREF_DIR',
            'maya': 'MAYA_APP_DIR',
            'nuke': 'NUKE_PATH'
        }

        extension = self.get_file_extension(file_path)

        if extension in ['.usd', '.usda']:
            open_in_usd_view(file_path)
            return
        
        application = self.get_application(extension)
        application_path = self.get_application_path(application)
        
        application_args = [application_path, file_path]
        env = os.environ.copy()
        
        pref_path = get_pref(application)
        
        if pref_path and os.path.exists(pref_path):
            pref_env_var = pref_dict[application]
            env[pref_env_var] = pref_path

        if application == "maya":
            env["QT_PLUGIN_PATH"] = r"C:\Program Files\Autodesk\Maya2023\plugins\platforms"
            env["PYTHONPATH"] = PINPIN_PATH

        if application == 'zbrush':
            file_path = file_path.replace('/', '\\')
            os.startfile(file_path)

        else:
            logger.info(f'Open {file_path} in {application}')
            subprocess.Popen(application_args, env = env)
            
        set_recent_file(file_path)
