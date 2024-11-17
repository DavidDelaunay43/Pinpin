from pathlib import Path
from typing import Union
from maya import cmds
from Packages.apps.maya_app.utils.workspace import set_project
from Packages.utils.core import Core
from Packages.utils.file_info import FileInfo
from Packages.utils.logger import Logger


class MayaFileInfo(FileInfo):


    EXT_DICT = {
        '.ma': 'mayaAscii',
        '.mb': 'mayaBinary'
    }


    def __init__(self, path: Path) -> None:
        super(MayaFileInfo, self).__init__(path)


    @property
    def backup_publish_file_path(self) -> Path:
        return self.find_next_backup_publish_file_path()


    @property
    def publish_file_name(self) -> str:
        return '_'.join(
            [
                *self.WORDS[:len(self.WORDS)-2],
                f'P{self.extension}'
            ]
        )


    @property
    def publish_file_path(self) -> Path: pass


    @property
    def maya_file_type(self) -> str:
        return self.EXT_DICT.get(self.extension)


    @property
    def maya_project(self) -> Path:
        return self.pipeline_path[len(self.pipeline_path.parts)] - self.pipeline_path.index('scenes')


    def set_maya_project(self) -> None:
        set_project()


    def get_word(self, index: int) -> Union[str, None]:
        return self.WORDS[index] if len(self.WORDS)>index else None
    

    def incremental_save(self, path_override: Path) -> None:
        path: Path = path_override if path_override else self.NEXT_PIPELINE_PATH
        cmds.file(rename=path)
        cmds.file(save=True, force=True, options="v=0", type=self.maya_file_type)
        Logger.info(f'Incremental save: {path}')
    

    def save_preview_image(self) -> None:
        
        output_image_path: Path = Core.project_data_paths().PREVIEW_DIRPATH.joinpath(f'{self.pipeline_name}.png')
        if output_image_path.exists():
            output_image_path.rmdir()

        cmds.select(clear=True)
        cmds.playblast(format = 'image', 
                   filename = str(output_image_path), 
                   sequenceTime = False, 
                   viewer = True, 
                   showOrnaments = False, 
                   frame = [0, 0], 
                   percent = 100, 
                   compression = 'png',
                   widthHeight = [128, 72],
                   quality = 50)
        

    def check_naming(self, word_num: int) -> None:
        if len(self.WORDS) == word_num:
            return
        Logger.warning(
                f'File name: {self.pipeline_name} must have {word_num} words.\nExemple: CDS_chr_marcel_geo_E_001.ma'
            )
        

    def find_next_backup_publish_file_path(self) -> Union[Path, None]:

        if not self.publish_file_path.exists():
            return

        old_dir: Path = self.publish_file_path.parent.joinpath('old')
        if not old_dir.exists():
            old_publish_file_name: str = '_'.join(
                [
                    *self.WORDS[:len(self.WORDS)-2],
                    'P',
                    f'001{self.extension}'
                ]
            )
            return old_dir.joinpath(old_publish_file_name)
        
        backup_num: int = len(
            [
                file_path
                for file_path in old_dir.iterdir()
                if file_path.name.startswith(self.publish_file_name.split('.')[0])
            ]
        ) +1
        old_publish_file_name: str = '_'.join(
            [
                *self.WORDS[:len(self.WORDS)-2],
                'P',
                f'{backup_num:03}{self.extension}'
            ]
        )
        return old_dir.joinpath(old_publish_file_name)
        

    def export_file(self, path_override: Union[Path, None] = None):
        path: Path = path_override if path_override else self.publish_file_path

        cmds.file(save=True)
        cmds.file(str(path), force=True, options="v=0", type=self.maya_file_type, exportSelected=True, preserveReferences=False)


    def publish_file(self, path_override: Union[Path, None] = None) -> None:

        if not cmds.ls(selection=True):
            cmds.warning('Select something to export.')
            return

        if not self.publish_file_path.exists():
            self.export_file(path_override=path_override)
            return
        
        old_dir: Path = self.publish_file_path.parent.joinpath('old')
        if not old_dir.exists():
            old_dir.mkdir()
        old_publish_file_path: Path = self.publish_file_path
        old_publish_file_path.rename(self.backup_publish_file_path)
        self.export_file()
        Logger.info(f'File exported: {self.publish_file_path}')
        Logger.info(f'Old publish backup: {self.backup_publish_file_path}')


class MayaAssetFileInfo(MayaFileInfo):


    asset_dict: dict = {
        'chr': '01_character',
        'prp': '02_prop',
        'itm': '03_item',
        'env': '04_env',
        'mod': '05_module',
        'drm': '06_diorama',
        'fx': '07_fx',
        'cam': '08_camera'
    }
    

    def __init__(self, path: Path):
        super(MayaAssetFileInfo, self).__init__(path)

        self.check_naming(6)


    @property
    def publish_file_path(self) -> Path:
        # PROJECT/09_publish/asset/01_character/geo/FKP_chr_marcel_geo_P.ma
        return Core.current_project_path().joinpath(
            '09_publish', 'asset', self.asset_dict[self.asset_type], self.department, self.publish_file_name
        )


    @property
    def project_prefix(self) -> str:
        return self.get_word(index=0)
    

    @property
    def asset_type(self) -> Union[str, None]:
        return self.get_word(index=1)
    

    @property
    def asset_name(self) -> Union[str, None]:
        return self.get_word(index=2)
    

    @property
    def department(self) -> Union[str, None]:
        return self.get_word(index=3)
    

    @property
    def step(self) -> Union[str, None]:
        return self.get_word(index=4)
    

    @property
    def version(self) -> Union[str, None]:
        return self.get_word(index=5)
    

class MayaSequenceFileInfo(MayaFileInfo):
    

    def __init__(self, path: Path):
        super(MayaSequenceFileInfo, self).__init__(path)

        self.check_naming(5)


    @property
    def publish_file_path(self) -> Path:
        # PROJECT/09_publish/asset/01_character/geo/FKP_chr_marcel_geo_P.ma
        return Core.current_project_path().joinpath(
            '09_publish', 'sequence', self.sequence_num, self.department, self.publish_file_name
        )


    @property
    def project_prefix(self) -> str:
        return self.get_word(index=0)
    

    @property
    def sequence_num(self) -> Union[str, None]:
        return self.get_word(index=1)
    

    @property
    def department(self) -> Union[str, None]:
        return self.get_word(index=2)
    

    @property
    def step(self) -> Union[str, None]:
        return self.get_word(index=3)
    

    @property
    def version(self) -> Union[str, None]:
        return self.get_word(index=4)


class MayaShotFileInfo(MayaFileInfo):
    

    def __init__(self, path: Path):
        super(MayaShotFileInfo, self).__init__(path)

        self.check_naming(6)


    @property
    def publish_file_path(self) -> Path:
        # PROJECT/09_publish/asset/01_character/geo/FKP_chr_marcel_geo_P.ma
        return Core.current_project_path().joinpath(
            '09_publish', 'shot', self.sequence_num, self.shot_num, self.department, self.publish_file_name
        )
    

    @property
    def cache_path(self) -> Path:
        return Core.current_project_path().joinpath(
            '11_cache', self.sequence_num, self.shot_num
        )


    @property
    def project_prefix(self) -> str:
        return self.get_word(index=0)
    

    @property
    def sequence_num(self) -> Union[str, None]:
        return self.get_word(index=1)
    

    @property
    def shot_num(self) -> Union[str, None]:
        return self.get_word(index=2)
    

    @property
    def department(self) -> Union[str, None]:
        return self.get_word(index=3)
    

    @property
    def step(self) -> Union[str, None]:
        return self.get_word(index=4)
    

    @property
    def version(self) -> Union[str, None]:
        return self.get_word(index=5)


def init_file_info(path: Path):

    path = Path(path) if not isinstance(path, Path) else path
    maya_ext: str = '.ma'

    if 'seq' in path.name and 'sh' in path.name and path.name.endswith(maya_ext):
        Logger.debug(f'SHOT SCENE: {path}')
        return MayaShotFileInfo(path)
    
    elif 'seq' in path.name and path.name.endswith(maya_ext):
        Logger.debug(f'SEQUENCE SCENE: {path}')
        return MayaSequenceFileInfo(path)
    
    elif path.name.endswith(maya_ext):
        Logger.debug(f'ASSET SCENE: {path}')
        return MayaAssetFileInfo(path)
    
    else:
        return FileInfo(path)
