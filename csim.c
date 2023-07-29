#include <stdio.h>
#include <stdlib.h>
#include <tgmath.h>

typedef struct {
  int valid;
  int tag_bits;
  int offset_bits;
} CacheLine;

typedef struct {
  CacheLine* cache_lines;
  int n_lines;
} CacheSet;

typedef struct {
  CacheSet* cache_sets;
  int n_sets;
} Cache;

Cache init_cache(int n_cache_sets, int n_cache_lines) {
  Cache cache;
  cache.n_sets = n_cache_sets;
  cache.cache_sets = (CacheSet*)malloc(cache.n_sets * sizeof(CacheSet));
  if (!cache.cache_sets) {
    // TODO: Then what
  }

  for (int i = 0; i < cache.n_sets; i++) {
    CacheSet cache_set;
    cache_set.n_lines = n_cache_lines;
    cache_set.cache_lines = (CacheLine*)malloc(cache_set.n_lines * sizeof(CacheLine));
    if (!cache_set.cache_lines) {
      // TODO: Then what
    }  
    cache.cache_sets[i] = cache_set;
  }
  return cache;


}

int main(int argc, char **argv) {
  int n_cache_sets = atoi(argv[1]);
  int n_cache_lines = atoi(argv[2]);

  Cache cache;

}

