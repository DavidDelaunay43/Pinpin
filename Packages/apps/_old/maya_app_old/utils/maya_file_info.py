from pathlib import Path
from typing import Union
from maya import cmds
from Packages.utils.core import Core
from Packages.utils.file_info import FileInfo
from Packages.utils.logger import Logger


class MayaFileInfo(FileInfo):


    def __init__(self, path: Path) -> None:
        super(MayaFileInfo, self).__init__(self, path)


    def get_word(self, index: int) -> Union[str, None]:
        return self.WORDS[index] if self.WORD_COUNT>index else None
    

    def incremental_save(self) -> None:
        cmds.file(rename=self.NEXT_PIPELINE_PATH)
        cmds.file(save=True)
        self.preview_image_path()
        Logger.info(f'Incremental save: {self.NEXT_PIPELINE_PATH}')


    def publish_export(self) -> None:
        if not cmds.ls(selection=True):
            cmds.error('Object to publish must be selected.')
            return
    

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


class MayaAssetFileInfo(MayaFileInfo):
    

    def __init__(self, path: Path):
        super(MayaAssetFileInfo, self).__init__(path)


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
    

    @property
    def department_publish_dir(self) -> Path:
        department: str = [self.department[:i] for i, char in enumerate(self.department) if char.isupper()][0]
        return Core.current_project_path().joinpath('09_publish', 'asset', department)
    

    @property
    def publish_file_name(self) -> str:
        return ('_').join([self.WORDS[:4], f'P{self.EXT}'])


    @property
    def publish_file_path(self) -> Path:
        return self.department_publish_dir.joinpath(self.publish_file_name)


class MayaSequenceFileInfo(MayaFileInfo):
    

    def __init__(self, path: Path):
        super(MayaSequenceFileInfo, self).__init__(path)


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
