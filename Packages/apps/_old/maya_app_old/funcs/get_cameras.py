from maya import cmds

def find_camera() -> list:

    camera_shapes = cmds.ls(type = 'camera')
    existing_cameras = ('persp', 'top', 'front', 'side')
    cameras = []

    for shape in camera_shapes:
        camera_transform  = cmds.listRelatives(shape, parent = True)[0]
        if not camera_transform in existing_cameras:
            cameras.append(camera_transform)

    return cameras