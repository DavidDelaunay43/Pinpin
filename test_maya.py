import maya.cmds as cmds
import maya.standalone as ms


def main() -> None:
    
    ms.initialize()
    cmds.polyCube()
    cmds.file(rename=r'C:\Users\DAVID\Desktop\TMPO.ma')
    cmds.file(save=True, type='mayaAscii')
    ms.uninitialize()


if __name__ == '__main__':
    main()
