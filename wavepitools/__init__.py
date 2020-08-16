from dataclasses import dataclass, field
from typing import Union, List

@dataclass
class Point(object):
    time_us: Union[int, float]
    state: bool

@dataclass
class Wave(object):
    points: List[Point] = field(default_factory=list)

    def remove_offset(self):
        if len(self.points) > 0:
            start_time = self.points[0].time_us
            for point in self.points:
                point.time_us = point.time_us - start_time
        
    def save_csv(self, file_name: str):
        with open(file_name, 'w') as file_ptr:
            for point in self.points:
                file_ptr.write("{0},{1}\n".format(point.time_us,int(point.state)))
    
    @classmethod
    def load_csv(cls, file_name: str):
        wave = cls()
        with open(file_name, 'r') as file_ptr:
            for line in file_ptr.readlines():
                data = line.split(',')
                wave.points.append(Point(int(data[0]), int(data[1])))
        return wave