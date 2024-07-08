import os


class AppFinder:
    
    
    PROGRAM_FILES = 'C:/Program Files'
    app_dict = {
        'blender': {'path': None, 'pref': None},
        'it': {'path': None, 'pref': None},
        'krita': {'path': None, 'pref': None},
        'houdini': {'path': None, 'pref': None},
        'mari': {'path': None, 'pref': None},
        'maya': {'path': None, 'pref': None},
        'nuke': {'path': None, 'pref': None},
        'photoshop': {'path': None, 'pref': None},
        'substance_designer': {'path': None, 'pref': None},
        'substance_painter': {'path': None, 'pref': None},
        'zbrush': {'path': None, 'pref': None}
    }
    
    
    def __init__(self) -> None:
            
        self.app_dict['blender']['path'] = self.find_blender()
        self.app_dict['krita']['path'] = self.find_krita()
        self.app_dict['houdini']['path'] = self.find_houdini()
        self.app_dict['mari']['path'] = self.find_mari()
        self.app_dict['maya']['path'] = self.find_maya()
        self.app_dict['nuke']['path'] = self.find_nuke()
        self.app_dict['photoshop']['path'] = self.find_photoshop()
        self.app_dict['zbrush']['path'] = self.find_zbrush()
        
        self.app_dict['houdini']['pref'] = self.find_houdini_pref()
        self.app_dict['mari']['pref'] = self.find_mari_pref()
        self.app_dict['maya']['pref'] = self.find_maya_pref()
        self.app_dict['nuke']['pref'] = self.find_nuke_pref()
        
    
    def find_directory(self, parent_directory: str, directory_string: str, return_type: str = 'str', exclude_strings = []) -> str:
        directories: list[str] = os.listdir(parent_directory)
        directories_to_return = []
        for dir in directories:
            if dir.startswith(directory_string):
                if dir in exclude_strings:
                        continue
                if return_type == 'str':
                    return dir
                else:
                    directories_to_return.append(dir)
        return directories_to_return
            
            
    def find_blender(self) -> str:
        exe: str = 'blender.exe'
        parent_dir: str = os.path.join(self.PROGRAM_FILES, 'Blender Foundation')
        dir_string: str = 'Blender '
        version_dir: str = self.find_directory(parent_directory=parent_dir, directory_string=dir_string)
        return os.path.join(parent_dir, version_dir, exe).replace('\\', '/')
    
    
    def find_krita(self) -> str:
        exe: str = 'krita.exe'
        parent_dir: str = os.path.join(self.PROGRAM_FILES, 'Krita (x64)')
        return os.path.join(parent_dir, 'bin', exe).replace('\\', '/')
    
    
    def find_houdini(self) -> str:
        exe: str = 'houdini.exe'
        parent_dir: str = os.path.join(self.PROGRAM_FILES, 'Side Effects Software')
        dir_string: str = 'Houdini'
        version_dir: str = self.find_directory(parent_directory=parent_dir, directory_string=dir_string, exclude_strings=['Houdini Engine', 'Houdini Server'])
        return os.path.join(parent_dir, version_dir, 'bin', exe).replace('\\', '/')
    
    
    def find_mari(self) -> str:
        mari: str = 'Mari'
        parent_dir: str = os.path.join(self.PROGRAM_FILES, self.find_directory(parent_directory=self.PROGRAM_FILES, directory_string=mari), 'Bundle', 'bin')
        exe: str = self.find_directory(parent_directory=parent_dir, directory_string=mari)
        return os.path.join(parent_dir, exe).replace('\\', '/')
    
    
    def find_maya(self) -> str:
        exe: str = 'maya.exe'
        parent_dir: str = os.path.join(self.PROGRAM_FILES, 'Autodesk')
        dir_string: str = 'Maya'
        version_dir: str = self.find_directory(parent_directory=parent_dir, directory_string=dir_string)
        return os.path.join(parent_dir, version_dir, 'bin', exe).replace('\\', '/')
    
    
    def find_nuke(self) -> str:
        nuke: str = 'Nuke'
        parent_dir: str = os.path.join(self.PROGRAM_FILES, self.find_directory(parent_directory=self.PROGRAM_FILES, directory_string=nuke))
        files: list[str] = self.find_directory(parent_directory=parent_dir, directory_string=nuke, return_type='list')
        exe: str
        for file in files:
            if file.endswith('.exe'):
                exe = file
                break
        return os.path.join(parent_dir, exe).replace('\\', '/')
    
    
    def find_photoshop(self) -> str:
        exe: str = 'Photoshop.exe'
        parent_dir: str = os.path.join(self.PROGRAM_FILES, 'Adobe')
        dir_string: str = 'Adobe Photoshop '
        version_dir: str = self.find_directory(parent_directory=parent_dir, directory_string=dir_string)
        return os.path.join(parent_dir, version_dir, exe).replace('\\', '/')
    
    
    def find_zbrush(self) -> str:
        exe: str = 'ZBrush.exe'
        parent_dir: str = os.path.join(self.PROGRAM_FILES, self.find_directory(parent_directory=self.PROGRAM_FILES, directory_string='Maxon ZBrush '))
        return os.path.join(parent_dir, exe).replace('\\', '/')


    def find_houdini_pref(self) -> str:
        documents_path = os.path.join(os.path.expanduser("~"), 'Documents')
        return os.path.join(documents_path, self.find_directory(documents_path, 'houdini'))
    
    
    def find_mari_pref(self) -> str:
        return os.path.join(os.path.expanduser("~"), '.mari')
    
    
    def find_maya_pref(self) -> str:
        documents_path = os.path.join(os.path.expanduser("~"), 'Documents')
        return os.path.join(documents_path, self.find_directory(documents_path, 'maya'))
    
    
    def find_nuke_pref(self) -> str:
        return os.path.join(os.path.expanduser("~"), '.nuke')


if __name__ == '__main__':
    import subprocess
    
    apps = AppFinder()
    print(apps.app_dict)
    
    for app, app_infos in apps.app_dict.items():
        exe = app_infos['path']
        if exe:
            if not os.path.exists(exe):
                continue
            print(exe)
            subprocess.Popen([exe])
