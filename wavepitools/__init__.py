from dataclasses import dataclass, field
from typing import Union, List

@dataclass
class Point(object):
    time_us: Union[int, float]
    state: bool

@dataclass
class Wave(object):
    points: List[Point] = field(default_factory=list)