from typing import NamedTuple
import math
from enum import Enum
from dataclasses import dataclass
from collections import deque
import itertools

# TODO: Add argparse for these parameters
S, E, B, m = (4, 1, 2, 4)

def tuple2string(tup):
    return ''.join(str(x) for x in tup)

# Emulate our address space
address_space = {address: tuple2string(tup) for address, tup in 
                  enumerate(itertools.product(range(2), repeat=m))}

class CacheLine:
    def __init__(self, blocks=None):
        self.blocks = blocks if blocks is not None else []
        self.tag = self.blocks[0][0] if self.blocks else None
        self.valid = 1 if self.blocks else 0

    def __getitem__(self, offset):
        return self.blocks[int(offset, 2)]

    def __contains__(self, tag):
        return self.tag == tag

    def __repr__(self):
        return (f'CacheLine(valid={self.valid}, ' 
                        f'tag={self.tag}, blocks={self.blocks})')

class CacheSet:
    def __init__(self):
        self.cache_lines = deque(maxlen=B)

    def __repr__(self):
        return f'CacheSet({self.cache_lines!r})'

    def match_line(self, tag):
        for line in self.cache_lines:
            if line.tag == tag and line.valid:
                return line
        return None

    def replace_line(self, address):
        """
        Replaces a cache line using the Least Recently Used (LRU) policy
        and returns the first block of the new cache line.
        """
        # TODO: Bounds check
        blocks = [address_space[address + i] for i in range(B)]
        # If full, just append to the right side of the deque
        # which will push out the least recently used (LRU) cache line
        self.cache_lines.append(CacheLine(blocks))
        return blocks[0]

class Cache:
    def __init__(self):
        self.sets = [CacheSet() for _ in range(S)]

        self._s = int(math.log2(S))
        self._b = int(math.log2(B))
        self._t = int(m - (self._b + self._s))

    def __getitem__(self, bitstring):
        idx = int(bitstring, 2)
        return self.sets[idx]

    def __repr__(self):
        return 'Cache(\n\t' + '\n\t'.join(repr(set_) for set_ in self.sets) + '\n)'

    def __call__(self, address):
        address_bits = address_space[address]
        tag, index_bits, offset_bits = self._parse_address(address_bits)
        cache_set = self[index_bits]
        cache_line = cache_set.match_line(tag)

        if cache_line:
            return cache_line[offset_bits]
        else:
            return cache_set.replace_line(address)

    def _parse_address(self, address_bits):
        tag = address_bits[:self._t]
        index_bits = address_bits[self._t:self._s]
        offset_bits = address_bits[self._s:]
        return (tag, index_bits, offset_bits)


if __name__ == '__main__':
    # S: Number of Cache Sets
    # E: Number of Cache Lines per Cache Set
    # B: Number of bytes per block
    # m: Word size of the system


    read_sequence = (0, 1, 13, 8, 0)

    cache = Cache()
    
    words = []
    for address in read_sequence:
        word = cache(address)
        print(word)
