#include <stdio.h>
#include <stdlib.h>
#include <tgmath.h>
#include <stdint.h>
#include <assert.h>

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;

#define IS_POW2(x) ((x % 2) == 0)

#define N_CACHE_SETS 4
static_assert(IS_POW2(N_CACHE_SETS), "N_CACHE_SETS must be a power of 2");

#define N_CACHE_LINES 2
static_assert(IS_POW2(N_CACHE_LINES), "N_CACHE_LINES must be a power of 2");

#define BYTES_PER_BLOCK 2
static_assert(IS_POW2(BYTES_PER_BLOCK), "BYTES_PER_BLOCK must be a power of 2");

#define WORD_SIZE 4
static_assert(IS_POW2(WORD_SIZE), "WORD_SIZE must be a power of 2");

typedef struct {
    u8 valid;
    u8 tag;
    u16 data[BYTES_PER_BLOCK];
} CacheLine;

typedef struct {
    CacheLine cache_lines;
} CacheSet;

int main(int argc, char **argv) {
    u8 index_bits = log2(N_CACHE_SETS);
    u8 offset_bits = log2(BYTES_PER_BLOCK);
    u8 tag_bits = 4 - (index_bits + offset_bits);

    CacheLine cache_line = { 0 };
    CacheSet cache_set = {.cache_lines = cache_line};

    u16 some_address = 0x32fe;

    cache_line.valid = 1;
    if (tag_bits == 1) {
        cache_line.tag = ;
    } else {
        cache_line.tag = some_address & (1 << ((u8)log2(tag_bits)));
    }
    

    //u8 mask = 1 << ((u8)(log2(tag_bits)));
    //cache_line.tag = some_address & (1 << (u8)log2(tag_bits));
    cache_line.data[offset_bits] = some_address;
}
