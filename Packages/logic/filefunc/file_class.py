import os
from Packages.logic.filefunc.utils import del_upper

class AssetFileInfos:

    def __init__(self, file_name: str) -> None:

        filename_noext, self.EXTENSION = os.path.splitext(file_name)
        infos = filename_noext.split("_")

        self.PROJECT = infos[0]
        self.ASSET_TYPE = infos[1]
        self.ASSET_NAME = infos[2]
        self.DEPARTMENT = del_upper(infos[3])
        self.STEP = infos[4]

        if self.STEP == 'E':
            self.INCREMENT = infos[5]
            
    def project(self):
        return self.PROJECT
    
    def asset_type(self):
        return self.ASSET_TYPE
    
    def asset_name(self):
        return self.ASSET_NAME
    
    def departement(self):
        return self.DEPARTMENT
    
    def step(self):
        return self.STEP
    
    def increment(self):
        return self.INCREMENT

class SequenceFileInfos:

    def __init__(self, file_name: str) -> None:

        filename_noext, self.EXTENSION = os.path.splitext(file_name)
        infos = filename_noext.split("_")

        self.PROJECT = infos[0]
        self.SEQUENCE = infos[1]
        self.DEPARTMENT = infos[2]
        self.STEP = infos[3]

        if self.STEP == 'E':
            self.INCREMENT = infos[4]
            
    def project(self):
        return self.PROJECT
    
    def sequence(self):
        return self.SEQUENCE
    
    def departement(self):
        return self.DEPARTMENT
    
    def step(self):
        return self.STEP
    
    def increment(self):
        return self.INCREMENT

class ShotFileInfos:

    def __init__(self, file_name: str) -> None:

        filename_noext, self.EXTENSION = os.path.splitext(file_name)
        infos = filename_noext.split("_")

        self.PROJECT = infos[0]
        self.SEQUENCE = infos[1]
        self.SHOT = infos[2]
        self.DEPARTMENT = infos[3]
        self.STEP = infos[4]

        if self.STEP == 'E':
            self.INCREMENT = infos[5]
            
    def project(self):
        return self.PROJECT
    
    def sequence(self):
        return self.SEQUENCE
    
    def shot(self):
        return self.SHOT
    
    def departement(self):
        return self.DEPARTMENT
    
    def step(self):
        return self.STEP
    
    def increment(self):
        return self.INCREMENT
