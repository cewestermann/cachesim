#include <stdio.h>
#include <stdlib.h>
#include <tgmath.h>
#include <stdint.h>
#include <assert.h>

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;

#define BITSIZE_OF(x) (sizeof(x) * 8)
#define IS_POW2(x) ((x % 2) == 0)

#define N_CACHE_SETS 4
static_assert(IS_POW2(N_CACHE_SETS), "N_CACHE_SETS must be a power of 2");

#define N_CACHE_LINES 4
static_assert(IS_POW2(N_CACHE_LINES), "N_CACHE_LINES must be a power of 2");

#define BYTES_PER_BLOCK 4
static_assert(IS_POW2(BYTES_PER_BLOCK), "BYTES_PER_BLOCK must be a power of 2");

#define WORD_SIZE 16
static_assert(IS_POW2(WORD_SIZE), "WORD_SIZE must be a power of 2");

typedef struct {
    u8 valid;
    u8 tag;
    u16 data[BYTES_PER_BLOCK];
} CacheLine;

typedef struct {
    CacheLine cache_lines;
} CacheSet;

u16 decimal2bitmask(u8 decimal) {
    u16 mask = 0;
    for (u8 i = 0; i < decimal; i++) {
        mask |= 1 << i;
    }
    return mask;
}

int main(int argc, char **argv) {
    u8 index_bits = log2(N_CACHE_SETS);
    u8 offset_bits = log2(BYTES_PER_BLOCK);
    u32 tag_bits = WORD_SIZE - (index_bits + offset_bits);

    CacheLine cache_line = { 0 };
    CacheSet cache_set = {.cache_lines = cache_line};

    u16 some_address = 0x32fe;
    u16 mask = decimal2bitmask(tag_bits);

    cache_line.valid = 1;
    // Set the tag of cacheline to be the first tag_bits of some_address
    cache_line.tag = some_address & (mask << (index_bits + offset_bits));
    cache_line.data[offset_bits] = some_address;
}


