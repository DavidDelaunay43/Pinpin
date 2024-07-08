import os
from Packages.utils.constants.pinpin import PINPIN_PATH
from Packages.utils.constants.preferences import CURRENT_PROJECT_JSON_PATH
from Packages.utils.funcs import get_current_value


BLANK_PINPIN_DATA = os.path.join(PINPIN_PATH, '.pinpin_data')
BLANK_pinpin_data_ICONS = os.path.join(BLANK_PINPIN_DATA, 'icons')
BLANK_pinpin_data_PREVIEW = os.path.join(BLANK_PINPIN_DATA, 'preview')
BLANK_pinpin_data_FILE_DATA = os.path.join(BLANK_PINPIN_DATA, 'file_data.json')
BLANK_pinpin_data_PREFIX = os.path.join(BLANK_PINPIN_DATA, 'prefix.json')
BLANK_pinpin_data_VARIANTS = os.path.join(BLANK_PINPIN_DATA, 'variants.json')

#
CURRENT_PROJECT = get_current_value(CURRENT_PROJECT_JSON_PATH, 'current_project', fail_return='str')
CURRENT_PROJECT_NAME = os.path.basename(CURRENT_PROJECT)

pinpin_data_PATH = os.path.join(CURRENT_PROJECT, '.pinpin_data')
pinpin_data_ICONS = os.path.join(pinpin_data_PATH, 'icons')
pinpin_data_PREVIEW = os.path.join(pinpin_data_PATH, 'preview')
pinpin_data_FILE_DATA = os.path.join(pinpin_data_PATH, 'file_data.json')
pinpin_data_PREFIX = os.path.join(pinpin_data_PATH, 'prefix.json')
pinpin_data_VARIANTS = os.path.join(pinpin_data_PATH, 'variants.json')
