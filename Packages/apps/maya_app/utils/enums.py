from enum import Enum


class Get(Enum):

    OPEN: str = 'Open'
    IMPORT: str = 'Import'
    REFERENCE: str = 'Reference'


class Namespace(Enum):

    NO_NAMESPACE: str = 'no namespace'
    FILE_NAMESPACE: str = 'file namespace'
    CUSTOM_NAMESPACE: str = 'custom namespace'


class GetMode(Enum):

    OPEN: str = Get.OPEN.value
    IMPORT: str = f'{Get.IMPORT.value} {Namespace.NO_NAMESPACE.value}'
    IMPORT_FILE_NAMESPACE: str = f'{Get.IMPORT.value} {Namespace.FILE_NAMESPACE.value}'
    IMPORT_CUSTOM_NAMESPACE: str = f'{Get.IMPORT.value} {Namespace.CUSTOM_NAMESPACE.value}'
    REFERENCE: str = f'{Get.REFERENCE.value} {Namespace.NO_NAMESPACE.value}'
    REFERENCE_FILE_NAMESPACE: str = f'{Get.REFERENCE.value} {Namespace.FILE_NAMESPACE.value}'
    REFERENCE_CUSTOM_NAMESPACE: str = f'{Get.REFERENCE.value} {Namespace.CUSTOM_NAMESPACE.value}'
