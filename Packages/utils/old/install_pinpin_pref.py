import os
import shutil
from Packages.utils.constants.constants_old import PREF_DEFAULT_PATH

shutil.copytree(PREF_DEFAULT_PATH, os.path.expanduser("~"))
