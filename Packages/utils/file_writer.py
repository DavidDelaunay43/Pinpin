from pathlib import Path


class FileWriter:


    def __init__(self, path: Path, string: str = None):
        
        if not string:
            return

        with open(path, 'r') as file:
            content = file.read()

        if string in content:
            return
        
        content = f'{content}\n{string}'
        
        with open(path, 'w') as file:
            file.write(content)
        
        return
