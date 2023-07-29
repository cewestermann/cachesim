from enum import Enum
from typing import NamedTuple

class Operation(Enum):
    INSTRUCTION = "I"
    LOAD = "L"
    STORE = "S"
    MODIFY = "M"

class Trace(NamedTuple):
    operation: Operation
    address: str
    size: int

    @classmethod
    def from_str(cls, str_):
        split = str_.split()
        op = Operation(split[0])
        address, size = split[1].split(',')
        return cls(op, address, size)

def read_trace(trace_name):
    with open(f'traces/{trace_name}.trace', 'r') as f:
        return f.read().split('\n')[:-1]

if __name__ == '__main__':
    pass
