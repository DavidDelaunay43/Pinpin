from pathlib import Path
from typing import Protocol, Union


class PipelineWidget(Protocol):
    
    
    _pipeline_path: Union[Path, None]
    
    
    @property
    def pipeline_path(self) :
        pass
    
    
    @pipeline_path.setter
    def pipeline_path(sefl):
        pass
    
    
    @property
    def pipeline_name(self):
        pass
    
    
    def populate_update_path(self):
        pass
    
    
    def populate(self):
        pass


class PipelineWidgetItem(Protocol):
    
    
    _pipeline_path: Path
    
    
    @property
    def pipeline_path(self) :
        pass
    
    
    @pipeline_path.setter
    def pipeline_path(sefl):
        pass
    
    
    @property
    def pipeline_name(self):
        pass
