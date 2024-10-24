import os
from Packages.utils.old.funcs import get_current_value
from Packages.utils.constants.user import USER_DIR
from Packages.utils.constants.pinpin import PINPIN_PATH

"""
- C:
    - ProgramFiles
        - Pinpin
            - .pinpin
                - logs
                - apps.json
                - clicked_items.json
                - recent_files.json
                - ui_prefs.json
                - version.json
    - Users
        - <username>
            - .pinpin
                - logs
                - apps.json
                - clicked_items.json
                - recent_files.json
                - ui_prefs.json
                - version.json
"""

# USER PREFERENCES

USER_PREFS = os.path.join(USER_DIR, '.pinpin')

LOGS_PATH = os.path.join(USER_PREFS, 'logs')
APPS_JSON_PATH = os.path.join(USER_PREFS, 'apps.json')
CLICKED_ITEMS_JSON_PATH = os.path.join(USER_PREFS, 'clicked_items.json')
CURRENT_PROJECT_JSON_PATH = os.path.join(USER_PREFS, 'current_project.json')
RECENT_FILES_JSON_PATH = os.path.join(USER_PREFS, 'recent_files.json')
UI_PREFS_JSON_PATH = os.path.join(USER_PREFS, 'ui_prefs.json')
VERSION_JSON_PATH = os.path.join(USER_PREFS, 'version.json')

CURRENT_PROJECT = get_current_value(json_file=CURRENT_PROJECT_JSON_PATH, key='current_project', fail_return='str')
RECENT_FILES = get_current_value(json_file=RECENT_FILES_JSON_PATH, key='recent_files', fail_return='str')
VERSION = get_current_value(json_file=CURRENT_PROJECT_JSON_PATH, key='version', fail_return='str')
NUM_FILES = get_current_value(json_file=UI_PREFS_JSON_PATH, key='num_files', fail_return='str')
REVERSE_SORT_FILES = get_current_value(UI_PREFS_JSON_PATH, 'reverse_sort_file')

# BLANK PREFERENCES

BLANK_PREFS = os.path.join(PINPIN_PATH, '.pinpin')

BLANK_LOGS_PATH = os.path.join(BLANK_PREFS, 'logs')
BLANK_APPS_JSON_PATH = os.path.join(BLANK_PREFS, 'apps.json')
BLANK_CLIKED_ITEMS_JSON_PATH = os.path.join(BLANK_PREFS, 'clicked_items.json')
BLANK_CURRENT_PROJECT_JSON_PATH = os.path.join(USER_PREFS, 'current_project.json')
BLANK_RECENT_FILES_JSON_PATH = os.path.join(BLANK_PREFS, 'recent_files.json')
BLANK_UI_PREFS_JSON_PATH = os.path.join(BLANK_PREFS, 'ui_prefs.json')
BLANK_VERSION_JSON_PATH = os.path.join(BLANK_PREFS, 'version.json')
