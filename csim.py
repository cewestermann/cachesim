from typing import NamedTuple
import math
from enum import Enum
from dataclasses import dataclass
from collections import deque
import itertools

m = 4 # Address size

def tuple2bitstring(tup):
    return ''.join(str(x) for x in tup)

# Emulate our address space
address_space = {address: tuple2bitstring(tup) for address, tup in 
                  enumerate(itertools.product(range(2), repeat=m))}

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

class CacheLine:
    def __init__(self, B):
        self.valid = 0
        self.tag = None
        self.blocks = []

    def __contains__(self, tag):
        return self.tag == tag

    def get_block(self, offset):
        return self.blocks[offset]

class CacheSet:
    def __init__(self, B):
        self.cache_line = CacheLine(B)

    def get_cache_line(self, tag):
        # TODO: Extend when we can have more than one cache line per
        # cache set.
        return self.cache_line

def parse_address(address, s, t):
    tag = address[:t]
    index_bits = address[t:s]
    offset_bits = address[s:]
    return (tag, index_bits, offset_bits)

class Cache:
    def __init__(self, S, B, m):
        self.sets = [CacheSet(B) for _ in range(S)]

    def __getitem__(self, bitstring):
        idx = int(bitstring, 2)
        return self.sets[idx]

if __name__ == '__main__':
    S, E, B, m = (4, 1, 2, 4)
    s = int(math.log2(S))
    b = int(math.log2(B))
    t = int(m - (b + s))

    read_sequence = (0, 1, 13, 8, 0)

    cache = Cache(S, B, m)
    
    words = []
    for address in read_sequence:
        address_bits = address_space[address]

        tag, index_bits, offset_bits = parse_address(address_bits, s, t)
        print(f"tag: {tag}\tindex_bits: {index_bits}\toffset_bits: {offset_bits}")
        cache_set = cache[index_bits]
        cache_line = cache_set.get_cache_line(tag)
        if cache_line:
            words.append(cache_line.get_block(offset_bits))
        else:
            cache_set.replace_line(address_bits)
#        break
#
