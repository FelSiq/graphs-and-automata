#ifndef __HEAP_H__
#define __HEAP_H__

typedef struct heap_struct heap;

heap *heap_start();
void *heap_pop(heap *h);
void heap_push(heap *h, float key, void *item);
void heap_destroy(heap **h);

#endif
