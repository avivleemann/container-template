
from dataclasses import dataclass
from pathlib import Path
import logging

@dataclass
class workDir:
    dir : Path = Path('__file__').resolve().parent
    figures : Path = dir / 'figures'
    data : Path = dir / 'data'
    results : Path = dir / 'results'
    logs : Path = dir / 'logs'
    
    __post_init__ = lambda self: [x.mkdir(parents=True, exist_ok=True) for x in self.__dict__.values() if isinstance(x, Path)]


@dataclass
class MyLogger:
    name: str
    log_file: str
    
    def __post_init__(self):
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        handler = logging.FileHandler(self.log_file, mode='w')
        handler.setFormatter(formatter)
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        
    @property
    def get(self)->logging.Logger:
        return self.logger
       