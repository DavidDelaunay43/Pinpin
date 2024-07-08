import os
from Packages.utils.constants.preferences import VERSION_JSON_PATH, BLANK_VERSION_JSON_PATH
from Packages.utils.funcs import get_current_value


VERSION = get_current_value(os.path.join(BLANK_VERSION_JSON_PATH), 'version')
USER_VERSION = get_current_value(os.path.join(VERSION_JSON_PATH), 'version')
