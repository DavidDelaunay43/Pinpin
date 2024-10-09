import os
from pathlib import Path
from subprocess import Popen
from typing import Union
from Packages.utils.core import Core
from Packages.utils.logger import Logger


class FileOpener:
    
    
    def __init__(self, path: Union[Path, None]) -> None:
        
        self._pipeline_path: Union[Path, None] = path
        self._soft_name: Union[str, None] = self._find_soft_name_from_ext()
        self._soft_path: Union[Path, None] = self._find_soft_paths_from_ext()[0]
        self._pref_path: Union[Path, None] = self._find_soft_paths_from_ext()[1]
        self._python_path: Union[Path, None] = self._find_soft_paths_from_ext()[2]
        
        
    @property
    def pipeline_path(self) -> Union[None, Path]:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Union[Path, None]) -> None:
        self._pipeline_path = path
        
        
    @property
    def pipeline_name(self) -> Union[str, None]:
        return self._pipeline_path.name if self._pipeline_path else None
    
    
    @property
    def software_name(self) -> Union[str, None]:
        return self._soft_name
    
    
    @property
    def sofware_path(self) -> Union[str, None]:
        return self._soft_path
    
    
    @property
    def pref_path(self) -> Union[Path, None]:
        return self._pref_path
    
    
    @property
    def python_path(self) -> Union[Path, None]:
        return self._python_path
    
    
    def update_infos(self, path: Union[Path, None]) -> None:
        self.pipeline_path = path
        if not path or not path.is_file():
            self._soft_name: Union[str, None] = None
            self._soft_path: Union[Path, None] = None
            self._pref_path: Union[Path, None] = None
            self._python_path: Union[Path, None] = None
            return
            
        self._soft_name = self._find_soft_name_from_ext()
        self._soft_path, self._pref_path, self._python_path = self._find_soft_paths_from_ext()
        Logger.info(f'Update infos:\nPipeline path: {self.pipeline_path}\nApp name: {self._soft_name}\nApp path: {self._soft_path}\nPrefs path: {self._pref_path}\nPython path: {self._python_path}')
        
    
    def _find_soft_name_from_ext(self) -> Union[str, None]:
        
        if not self.pipeline_path or not self.pipeline_path.is_file():
            return
        
        extension: str = self.pipeline_path.suffix
        if not extension in Core.EXTS.keys():
            return
        
        return Core.EXTS.get(self.pipeline_path.suffix)
    
    
    def _find_soft_paths_from_ext(self) -> Union[tuple[Path], tuple[None]]:
        
        apps_dict: dict = Core.prefs_paths().APPS_JSONFILE.json_to_dict()
        
        if not self.software_name in apps_dict.keys():
            return None, None, None
        
        app_dict: dict = apps_dict.get(self.software_name.lower())
        
        path: Union[str, None] = app_dict.get('path')
        path = Path(path) if isinstance(path, str) else None
        
        pref: Union[str, None] = app_dict.get('pref')
        pref = Path(pref) if isinstance(pref, str) else None
        
        python_path: Union[str, None] = app_dict.get('python_path')
        python_path = Path(python_path) if isinstance(python_path, str) else None
        
        return path, pref, python_path
    
    
    def open_file(self) -> None:
        
        if self.software_name == 'zbrush':
            os.startfile(str(self.pipeline_path))
            Logger.info(f'Open file:\nFile path: {self.pipeline_path}\nApp path: {self.software_name}')
            return
        
        pref_dict: dict = {
            'houdini': 'HOUDINI_USER_PREF_DIR',
            'maya': 'MAYA_APP_DIR',
            'nuke': 'NUKE_PATH'
        }
        
        if not self.software_name in pref_dict.keys():
            Popen([self.pipeline_path])
            return

        application_args: list[Path] = [self.sofware_path, self.pipeline_path]
        env: dict[str, str] = os.environ.copy()
        
        if self.pref_path:
            env[pref_dict.get(self.software_name)] = str(self.pref_path)
            
        if self.python_path:
            env['PYTHONPATH'] = str(self.python_path)
            
        Popen(application_args, env=env)
        Logger.info(f'Open file:\nFile path: {self.pipeline_path}\nApp path: {self.software_name}\nPref path: {self.pref_path}\nPython path: {self.python_path}')
