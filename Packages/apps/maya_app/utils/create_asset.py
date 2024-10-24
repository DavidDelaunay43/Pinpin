__authors__ = 'Émile Ménard', 'David Delaunay'

from pathlib import Path
import shutil
from maya import cmds
from Packages.utils.core import Core
from Packages.utils.logger import Logger


class CreateAsset:


    TYPE_DICT: dict = {
        '01_character': 'chr',
        '02_prop': 'prp',
        '03_item': 'itm',
        '04_enviro': 'env',
        '05_module': 'mod',
    }
    SCENES: str = 'scenes'


    def __init__(self, asset_name: str, asset_type: str, project_name: str, subfolders: list[str], departments: list[str]) -> None:
        
        self._asset_name: str = asset_name.lower()
        self._asset_type: str = asset_type
        self._project_name: str = project_name.lower()
        self._subfolders: list[str] = subfolders
        self._departments: list[str] = departments


    @property
    def asset_name(self) -> str:
        return self._asset_name
    

    @property
    def asset_type(self) -> str:
        return self._asset_type
    

    @property
    def project_name(self) -> str:
        return self._project_name
    

    @property
    def subfolders(self) -> list[str]:
        return self._subfolders if self.SCENES in self._subfolders else self._subfolders.append(self.SCENES)
    

    @property
    def departments(self) -> list[str]:
        return self._departments
    

    def create(self) -> None:
        asset_dir: Path = Core.current_project_path().joinpath('04_asset')

        maya_project_dir: Path = asset_dir.joinpath(self.asset_type, self.asset_name, self.project_name)
        maya_project_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy(Core.workspace_mel(), maya_project_dir)

        for subfolder in self.subfolders:
            subfolder_dir: Path = maya_project_dir.joinpath(subfolder)
            subfolder_dir.mkdir(parents=True, exist_ok=True)

            if not subfolder==self.SCENES:
                continue

            for department in self.departments:
                subfolder_dir.joinpath(department).mkdir(parents=True, exist_ok=True)

        Logger.info(f'Create Asset:\nasset type: {self.asset_type}\nasset name: {self.asset_name}\nproject name: {self.project_name}\nsubfolders: {self.subfolders}\ndepartments: {self.departments}')

        if 'geo' in self.departments:
            prefix: str = Core.project_data().PREFIX
            type: str = self.TYPE_DICT.get(self.asset_type)
            geo_dir: Path = maya_project_dir.joinpath('scenes', 'geo')
            geo_name: str = f'{prefix}_{type}_{self.asset_name}_geo_E_001.ma'
            geo_path: Path = geo_dir.joinpath(geo_name)
            cmds.file(rename=geo_path)
            cmds.file(save=True)

        Logger.info(f'Save scene as: {geo_path}')
