from pathlib import Path
from maya import cmds
from Packages.apps.maya_app.utils.maya_file_info import MayaShotFileInfo


class AlembicSetUp:


    def __init__(self, object_sets: list[str]) -> None:
        
        self._pipeline_path: Path = Path(cmds.file(query=True, sceneNane=True))
        self._shot_file_info: MayaShotFileInfo = MayaShotFileInfo(self.pipeline_path)
        self._cache_path: Path = self._shot_file_info.cache_path
        self.abc_files: dict[str, Path] = self.get_abc_file_paths(object_sets)


    @property
    def pipeline_path(self) -> Path:
        return self._pipeline_path
    

    @property
    def shot_file_info(self) -> MayaShotFileInfo:
        return self._shot_file_info


    @property
    def cache_path(self) -> Path:
        return self._cache_path


    def get_abc_file_path(self, object_set: str) -> Path:
        """
        Example : 
            - FKP_seq10_sh020_fish_anim.abc
        """

        if not ':' in object_set:
            cmds.error(f'ObjectSet {object_set} must have a namespace (char name, prop name...)')

        prefix: str = self.shot_file_info.project_prefix
        sequence_num: str = self.shot_file_info.sequence_num
        shot_num: str = self.shot_file_info.shot_num
        name: str = object_set.split(':')[0]
        department: str = self.shot_file_info.department
        ext: str = '.abc'

        return self.cache_path.joinpath(
            f'{prefix}_{sequence_num}_{shot_num}_{name}_{department}{ext}'
        )


    def get_abc_file_paths(self, object_sets: list[str]) -> dict[str, Path]:
        
        abc_file_paths: dict = {}
        for object_set in object_sets:
            abc_file_paths[object_set] = self.get_abc_file_path(object_set)
        return abc_file_paths
    

    def export(self, object_set: str, abc_file_path: Path, start_frame: int = None, end_frame: int = None) -> None:

        start = start_frame if start_frame else cmds.playbackOptions(query = True, minTime = True)
        end = end_frame if end_frame else cmds.playbackOptions(query = True, maxTime = True)

        roots: str = ''
        for geo in cmds.sets(object_set, query=True, nodesOnly=True):
            roots += f'-root {geo}'

        job_arg: str = f'-frameRange {start} {end} -uvWrite -worldSpace -writeVisibility -writeUVSets -dataFormat ogawa {roots} -file {abc_file_path}'
        cmds.AbcExport(jobArg=job_arg)


    def export_all(self) -> None:

        for object_set, abc_file_path in self.abc_files.items():
            self.export(object_set, abc_file_path)
