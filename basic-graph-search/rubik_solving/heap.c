#include <heap.h>

typedef struct {
	void *item;
	float key;
} heap_node;

struct heap_struct {
	heap_node *heap;
	unsigned long int size;
}

heap *heap_start() {
	heap *h = malloc(sizeof(heap));
	if (h != NULL) {
		h->heap = NULL;
		h->size = 0;
	}
	return h;
}
void *heap_pop(heap *h);
void heap_push(heap *h, float key, void *item);

void heap_destroy(heap **h) {
	if (h != NULL && *h != NULL) {
		free(*h);
		*h = NULL;
	}
}
