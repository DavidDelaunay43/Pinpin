from urllib.parse import urljoin
import webbrowser


class Documentation:
    
    ROOT_URL: str = 'https://pinpin.readthedocs.io/en/latest/'
    PIPELINE_FILE: str = 'pipeline.html'
    STANDALONE_FILE: str = 'standalone.html'
    MAYA_FILE: str = 'maya.html'
    HOUDINI_FILE: str = 'houdini.html'
    
    @classmethod
    def open(cls, topic: str = '') -> None:
        webbrowser.open(urljoin(cls.ROOT_URL, topic))


def main() -> None:
    Documentation.open(Documentation.MAYA_FILE)
    
    
if __name__ == '__main__':
    main()
