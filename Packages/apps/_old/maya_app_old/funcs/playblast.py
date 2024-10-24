import os
from maya import cmds
from Packages.utils.constants.constants_old import CURRENT_PROJECT_PREVIEW_FOLDER
from Packages.utils.logger import init_logger

logger = init_logger(__file__)

def rename_thumbnail(file_path: str):
    '''
    '''
    file_path = f'{file_path}.png'
    if not os.path.exists(file_path):
        logger.info(f'{file_path} does not exist.')
        return
    
    logger.info(f'{file_path} already exists.')
    base_file_path, png = os.path.splitext(file_path)
    base, ext = os.path.splitext(base_file_path)
    i = 1
    new_name = f"{base}_{i:03}{ext}{png}"

    while os.path.exists(new_name):
        i += 1
        new_name = f"{base}_{i:03}{ext}{png}"

    os.rename(file_path, new_name)
    logger.info(f'{file_path} has been renamed : {new_name}')

def create_thumbnail(file_name: str, increment: bool = False, ext: str = '.ma'):
    '''
    '''

    output_image_path = os.path.join(CURRENT_PROJECT_PREVIEW_FOLDER, file_name)

    if increment:
        rename_thumbnail(output_image_path)

    cmds.select(clear = True)

    cmds.playblast(format = 'image', 
                   filename = output_image_path, 
                   sequenceTime = False, 
                   viewer = True, 
                   showOrnaments = False, 
                   frame = [0, 0], 
                   percent = 100, 
                   compression = 'png',
                   widthHeight = [180, 101],
                   quality = 50)
    
    output_image_path = output_image_path.replace(ext, f"{ext}.0000.png")
    os.rename(output_image_path, output_image_path.replace(".0000.", "."))

def update_thumbnail():
    '''
    '''

    current_file_path = cmds.file(query = True, sceneName = True)
    current_file_name = os.path.basename(current_file_path)

    thumbnail_file_name = f'{current_file_name}.png'
    thumnail_file_path = os.path.join(CURRENT_PROJECT_PREVIEW_FOLDER, thumbnail_file_name)

    if os.path.exists(thumnail_file_path):
        os.remove(thumnail_file_path)

    create_thumbnail(current_file_name)
    logger.info(f'{thumbnail_file_name} updated.')
