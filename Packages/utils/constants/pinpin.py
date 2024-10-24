import os
from Packages.utils.old.funcs import find_package_path


ROOT_NAME = 'Pinpin'  
PINPIN_PATH = find_package_path(ROOT_NAME)
PACKAGES_PATH = os.path.join(PINPIN_PATH, 'Packages')