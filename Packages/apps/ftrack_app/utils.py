import os
import ftrack_api
from Packages.logic.filefunc.file_class import AssetFileInfos

def guess_ftrack_task(file_path: str):
    """
    CDS_chr_petru_rig_E_001.ma
    """
    
    file_name = os.path.basename(file_path)
    asset = AssetFileInfos(file_name)
    asset_name = asset.asset_name()
    department = asset.departement()