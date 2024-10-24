__authors__ = 'Apolline Royer', 'David Delaunay'


from pathlib import Path
from typing import Union
from maya import cmds
from Packages.apps.maya_app.utils.enums import GetMode


class MayaFileGetter:


    def __init__(self, path: Union[Path, None], mode: GetMode, custom_namespace: Union[str, None] = None) -> None:
        
        if path and not path.exists():
            raise FileNotFoundError(f'{path} does not exists.')

        self._pipeline_path: Path = path
        self._mode: GetMode = mode
        self._custom_namespace: str = custom_namespace
        self.MODE_DICT: dict = {
            GetMode.OPEN: self.open_file,
            GetMode.IMPORT: self.import_file,
            GetMode.IMPORT_FILE_NAMESPACE: self.import_file_with_file_namespace,
            GetMode.IMPORT_CUSTOM_NAMESPACE: self.import_file_with_custom_namespace,
            GetMode.REFERENCE: self.referece_file,
            GetMode.REFERENCE_FILE_NAMESPACE: self.reference_file_with_file_namespace,
            GetMode.REFERENCE_CUSTOM_NAMESPACE: self.reference_file_with_custom_namespace
        }


    @property
    def pipeline_path(self) -> Union[Path, None]:
        return self._pipeline_path
    

    @pipeline_path.setter
    def pipeline_path(self, path: Union[Path, None]) -> None:
        self._pipeline_path = path
    

    @property
    def mode(self) -> GetMode:
        return self._mode
    

    @mode.setter
    def mode(self, new_mode: GetMode) -> None:
        self._mode = new_mode
    

    @property
    def custom_namespace(self) -> str:
        return self._custom_namespace
    

    @custom_namespace.setter
    def custom_namespace(self, text: str) -> None:
        self._custom_namespace = text
    

    def get_file(self) -> None:
        self.MODE_DICT.get(self.mode, GetMode.OPEN)()
    

    def open_file(self) -> None:
        cmds.file(self.pipeline_path, open=True, force=True)


    def import_file(self) -> None:
        cmds.file(self.pipeline_path, i=True, namespace=':', mergeNamespacesOnClash=True)


    def import_file_with_file_namespace(self) -> None:
        cmds.file(self.pipeline_path, i=True, namespace=self.pipeline_path.name.split('.')[0])


    def import_file_with_custom_namespace(self) -> None:
        cmds.file(self.pipeline_path, i=True, namespace=self.custom_namespace)


    def referece_file(self) -> None:
        cmds.file(self.pipeline_path, reference=True, namespace=":", mergeNamespaceWithRoot=True, mergeNamespacesOnClash=True, sharedNodes = "shadingNetworks")


    def reference_file_with_file_namespace(self) -> None:
        cmds.file(self.pipeline_path, reference=True, namespace=self.pipeline_path.name.split('.')[0], sharedNodes = "shadingNetworks")


    def reference_file_with_custom_namespace(self) -> None:
        cmds.file(self.pipeline_path, reference=True, namespace=self.custom_namespace, sharedNodes = "shadingNetworks")
