from pathlib import Path


class FileWriter:


    def __init__(self, path: Path, string: str = None, line_index: int = None):

        if not path.exists() or not string:
            return
        
        self._file_path = path if isinstance(path, Path) else Path(path)
        self._string = string
        self._line_index = line_index

        if not self._line_index:
            self._add_string()
            return
        
        self._replace_string()


    def _add_string(self) -> None:
        with self._file_path.open(mode='r', encoding='utf-8') as file:
            existing_lines = file.read().splitlines()

        if self._string in existing_lines:
            return

        with self._file_path.open(mode='a', encoding='utf-8') as file:
            file.write(self._string + '\n')

            
    def _replace_string(self) -> None:
        with self._file_path.open(mode='r', encoding='utf-8') as file:
            lines: list[str] = file.readlines()

        lines[self._line_index] = self._string + '\n'

        with self._file_path.open(mode='w', encoding='utf-8') as file:
            file.writelines(lines)
