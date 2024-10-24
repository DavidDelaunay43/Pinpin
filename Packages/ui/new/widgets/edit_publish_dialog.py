from pathlib import Path
from typing import Literal
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from Packages.utils.enums import State
from Packages.utils.file_info import FileInfo


class EditPublishDialog(QDialog):


    def __init__(self, path: Path, parent = None, state: State = State.EDIT):
        super(EditPublishDialog, self).__init__(parent)

        self.pipeline_path: Path = path
        self.file_info: FileInfo = FileInfo(path=path)

        QLabel(self.file_info.pipeline_name)
        QLabel(self.file_info.NEXT_PIPELINE_PATH) if state == State.EDIT else QLabel(self.file_info.publi)


def main() -> None:
    pass


if __name__ == '__main__':
    main()
