from pathlib import Path
from subprocess import Popen
import sys
from Packages.utils.logger import Logger


class Update:


    RELEASE_URL: str = 'https://api.github.com/repos/DavidDelaunay43/Pinpin/releases'
    DOWNLOAD_URL: str = 'https://github.com/DavidDelaunay43/Pinpin/releases/download'
    LAST_VERSION: str = ''


    @classmethod
    def installer_name(cls) -> str:
        return f'Pinpin_{cls.LAST_VERSION}_SetupWindows.exe'
    

    @classmethod
    def installer_url(cls) -> str:
        return f'{cls.DOWNLOAD_URL}/{cls.LAST_VERSION}/{cls.installer_name()}'


    @classmethod
    def installer_path(cls) -> Path:
        return Path.home().joinpath('Downloads', cls.installer_name())
    

    @classmethod
    def get_last_version(cls) -> str:
        import requests
        response = requests.get(cls.RELEASE_URL)
        if response.status_code == 200:
            version_name: str = response.json()[0].get('name')
            cls.LAST_VERSION = version_name
            return version_name


    @classmethod
    def download_installer(cls) -> None:
        import requests
        installer_url: str = cls.installer_url()
        response = requests.get(installer_url)
        Logger.debug(f'Download {installer_url} ...')

        if response.status_code == 200:
            with open(cls.installer_path(), 'wb') as file:
                file.write(response.content)
            print('Download successful !')
        else:
            print(f'Download failed.\nStatus: {response.status_code}')


    @classmethod
    def run_installer(cls) -> None:
        intaller_path: Path = cls.installer_path()
        Popen(intaller_path)
        Logger.debug(f'Run {intaller_path} ...')
        sys.exit()
