from typing import NamedTuple
import math
from enum import Enum
from dataclasses import dataclass
from collections import deque
import pprint
import itertools

# TODO: Add argparse for these parameters

# S: Number of Cache Sets
# E: Number of Cache Lines per Cache Set
# B: Number of bytes per block
# m: Word size of the system
S, E, B, m = (8, 4, 4, 8)

INDEX_BITS = int(math.log2(S))
OFFSET_BITS = int(math.log2(B))
TAG_BITS = m - (INDEX_BITS + OFFSET_BITS)

def tuple2string(tup):
    return ''.join(str(x) for x in tup)

# Emulate our address space
ADDRESS_SPACE = {address: tuple2string(tup) for address, tup in 
                  enumerate(itertools.product(range(2), repeat=m))}

class CacheLine:
    def __init__(self, blocks=None):
        self.blocks = blocks if blocks is not None else []
        self.tag = self.blocks[0][:TAG_BITS] if self.blocks else None
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

    def _push_to_front(self, idx):
        value = self.cache_lines[idx]
        # remove value at index
        self.cache_lines.remove(value)
        # append to the right side of the deque
        self.cache_lines.append(value)

    def match_line(self, tag):
        for idx, line in enumerate(self.cache_lines):
            if line.tag == tag and line.valid:
                self._push_to_front(idx)
                return line
        return None

    def replace_line(self, address):
        """
        Replaces a cache line using the Least Recently Used (LRU) policy
        and returns the first block of the new cache line.
        """
        # Check that address + i does not exceed the address space
        if address + B > len(ADDRESS_SPACE):
            blocks = [ADDRESS_SPACE[address + i] for i in range(len(ADDRESS_SPACE) - address)]
        else:
            blocks = [ADDRESS_SPACE[address + i] for i in range(B)]

        # Just append to the right side of the deque
        # which will push out the least recently used (LRU) cache line
        self.cache_lines.append(CacheLine(blocks))
        return blocks[0]

class Cache:
    def __init__(self):
        self.sets = [CacheSet() for _ in range(S)]
    def __getitem__(self, bitstring):
        idx = int(bitstring, 2)
        return self.sets[idx]

    def __repr__(self):
        return 'Cache(\n\t' + '\n\t'.join(repr(set_) for set_ in self.sets) + '\n)'

    def __call__(self, address):
        address_bits = ADDRESS_SPACE[address]
        tag, index_bits, offset_bits = self._parse_address(address_bits)
        cache_set = self[index_bits]
        cache_line = cache_set.match_line(tag)

        if cache_line:
            # TODO: If the cache_line exists, move to front of deque
            return cache_line[offset_bits]
        else:
            return cache_set.replace_line(address)

    def _parse_address(self, address_bits):
        tag = address_bits[:TAG_BITS]
        index_bits = address_bits[TAG_BITS:TAG_BITS + INDEX_BITS]
        offset_bits = address_bits[TAG_BITS + INDEX_BITS:]
        return (tag, index_bits, offset_bits)


if __name__ == '__main__':
    read_sequence = (0, 1, 13, 8, 0)

    cache = Cache()
    
    pprint.pprint(ADDRESS_SPACE)
    for address in read_sequence:
        word = cache(address)
        print(cache)
        print('\n')

