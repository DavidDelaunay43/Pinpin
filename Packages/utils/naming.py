from dataclasses import dataclass


@dataclass(frozen=True)
class PipeRoot:
    
    ASSET: str = '04_asset'
    SEQUENCE: str = '05_sequence'
    SHOT: str = '06_shot'
    COMP: str = '07_comp'
    EDITING: str = '08_editing'
    PUBLISH: str = '09_publish'
    TEXTURE: str = '10_texture'
    CACHE: str = '11_cache'


class PublishRoot:

    ASSET: str = 'asset'
    SEQUENCE: str = 'sequence'
    SHOT: str = 'shot'


class AssetRoot:
    
    CHARACTER: str = '01_character'
    PROP: str = '02_prop'
    ITEM: str = '03_item'
    ENVIRO: str = '04_enviro'
    MODULE: str = '05_module'
    DIORAMA: str = '06_diorama'
    FX: str = '07_fx'
    CAMERA: str = '08_camera'


class AssetAlias:
    
    CHARACTER: str = 'chr'
    PROP: str = 'prp'
    ITEM: str = 'itm'
    ENVIRO: str = 'env'
    MODULE: str = 'mod'
    DIORAMA: str = 'drm'
    CAMERA: str = 'cam'
    

class AssetDepartment:
    
    GEO: str = 'geo'
    LOOKDEV: str = 'ldv'
    RIG: str = 'rig'
    
    
class ShotDepartment:
    
    ANIM: str = 'anim'
    CONFO: str = 'confo'
    CLOTH: str = 'cloth'
    FX: str = 'fx'
    LAYOUT: str = 'layout'
    LIGHTING: str = 'lighting'
    RENDER: str = 'render'


def main() -> None:
    
    print(AssetRoot.CHARACTER)
    print(AssetAlias.CHARACTER)
    
    print(AssetRoot.ENVIRO)
    print(AssetAlias.ENVIRO)
    
    
if __name__ == '__main__':
    main()
    