from dataclasses import dataclass
from pathlib import Path
from typing import Union
from Packages.utils.json_file import JsonFile


@dataclass
class ProjectDataPaths:
    
    PROJECT_PATH: Union[Path, str]
    
    def __post_init__(self):
        
        self.PROJECT_PATH = Path(self.PROJECT_PATH) if not isinstance(self.PROJECT_PATH, Path) else self.PROJECT_PATH
        self.PINPIN_DATA_DIRPATH = self.PROJECT_PATH.joinpath('.pinpin_data')
        self.PREVIEW_DIRPATH: Path = self.PINPIN_DATA_DIRPATH.joinpath('preview')
        self.FILE_DATA_JSONFILE: JsonFile = JsonFile(path=self.PINPIN_DATA_DIRPATH.joinpath('file_data.json'))
        self.PREFIX_JSONFILE: JsonFile = JsonFile(path=self.PINPIN_DATA_DIRPATH.joinpath('prefix.json'))


@dataclass(frozen=True)
class ProjectData:
    
    FILE_DATA_DICT: dict
    PREFIX: str


@dataclass(frozen=True)
class SoftwarePaths:
    
    INTEGRATION_PATH: Path
    PINPIN_MENU_SOURCE_PATH: Path
    PINPIN_SHELF_SOURCE_PATH: Path
    
    PREFERENCES_PATH: Path
    PINPIN_MENU_DEST_PATH: Path
    PINPIN_SHELF_DEST_PATH: Path
            

@dataclass
class PreferencesPaths:
    
    USER_PREFS_ROOT: Path
    
    def __post_init__(self):
        
        self.LOGS_DIRPATH: Path = self.USER_PREFS_ROOT.joinpath('logs')
        self.APPS_JSONFILE: JsonFile = JsonFile(self.USER_PREFS_ROOT.joinpath('apps.json'))
        self.CURRENT_PROJECT_JSONFILE: JsonFile = JsonFile(self.USER_PREFS_ROOT.joinpath('current_project.json'))
        self.FAKE_PROJECT_DIRPATH: Path = self.USER_PREFS_ROOT.joinpath('FakeProject')
        self.MEMO_PATH_JSONFILE: JsonFile = JsonFile(self.USER_PREFS_ROOT.joinpath('memo_path.json'))
        self.RECENT_FILES_JSONFILE: JsonFile = JsonFile(self.USER_PREFS_ROOT.joinpath('recent_files.json'))
        self.UI_PREFS_JSONFILE: JsonFile = JsonFile(self.USER_PREFS_ROOT.joinpath('ui_prefs.json'))
        self.VERSION_JSONFILE: JsonFile = JsonFile(self.USER_PREFS_ROOT.joinpath('version.json'))

    
@dataclass(frozen=True)
class PreferencesInfos:
    
    CURRENT_PROJECT: Path
    LAST_PATHS: list
    RECENT_FILES: list
    NUM_FILES: int
    REVERSE_SORT_FILES: bool
    DEV_MODE: bool
    VERSION: str
    

@dataclass
class ShotFormat:
    
    sequence_num: int = None
    shot_num: int = None
    department: str = None
    
    def __post_init__(self):
        
        self.sequence_num = f'seq{self.sequence_num:03}' if self.sequence_num else ''
        self.shot_num = f'sh{self.shot_num:03}' if self.shot_num else ''
        self.shot_string = '_'.join([item for item in [self.sequence_num, self.shot_num, self.department] if item])


def main() -> None:
    
    shot: ShotFormat = ShotFormat(sequence_num=20, shot_num=30, department='anim')
    print(shot.sequence_num)
    print(shot.shot_num)
    print(shot.shot_string)
