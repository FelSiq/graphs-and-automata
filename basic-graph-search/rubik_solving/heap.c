#include <stdlib.h>
#include <stdio.h>
#include <heap.h>

#define HEAP_DEBUG 0

typedef struct {
	void *item;
	float key;
} heap_node;

struct heap_struct {
	heap_node *heap;
	unsigned long int size;
};

heap *heap_start() {
	heap *h = malloc(sizeof(heap));
	if (h != NULL) {
		h->heap = NULL;
		h->size = 0;
	}
	return h;
}

void *heap_pop(heap *h) {
	heap_node *heap_head = h->heap;
	void *item = heap_head->item;

	register unsigned long cur_position = 0, min_index,
		lchild_index = HEAP_LCHILD(cur_position), 
		rchild_index = HEAP_RCHILD(cur_position);
	register const unsigned long cur_size = --h->size;

	heap_node aux;

	// Swap head node with tail node
	aux = h->heap[0];
	h->heap[0] = h->heap[cur_size];
	h->heap[cur_size] = aux;

	// Don't want to lose performance for just few bytes
	// that will probably be used afterwards
	//h->heap = realloc(h->heap, sizeof(heap_node) * cur_size);

	// Downgrade "new head node" to its respective place
	while (lchild_index < cur_size) {

		if (rchild_index < cur_size && 
			h->heap[rchild_index].key < h->heap[lchild_index].key) {
			min_index = rchild_index;
		} else {
			min_index = lchild_index;
		}

		if (h->heap[min_index].key < h->heap[cur_position].key) {
			// If min_index element has a smaller key than the
			// current one, swap.
			aux = h->heap[cur_position];
			h->heap[cur_position] = h->heap[min_index];
			h->heap[min_index] = aux;

			cur_position = min_index;
			lchild_index = HEAP_LCHILD(cur_position), 
			rchild_index = HEAP_RCHILD(cur_position);
		} else {
			// Else, break main loop
			lchild_index = cur_size;
		}
	}

	return item;
}

void heap_push(heap *h, float key, void *item) {
	const register unsigned long int cur_size = h->size;
	register unsigned long int cur_position = cur_size;

	h->heap = realloc(h->heap, sizeof(heap_node) * (cur_size + 1));
	h->heap[cur_size].item = item;
	h->heap[cur_size].key = key;

	heap_node aux;
	register heap_node
		*master_node = h->heap + HEAP_MASTER(cur_position), 
		*cur_node = h->heap + cur_position;

	while (master_node->key > cur_node->key) {
		aux = *cur_node;
		*cur_node = *master_node;
		*master_node = aux;

		cur_position = HEAP_MASTER(cur_position);
		master_node = h->heap + HEAP_MASTER(cur_position);
		cur_node =  h->heap + cur_position;
	} 

	h->size++;
}

void heap_destroy(heap **h) {
	if (h != NULL && *h != NULL) {
		if ((*h)->heap != NULL) {
			while ((*h)->size--) {
				if ((*h)->heap[(*h)->size].item != NULL)
					free((*h)->heap[(*h)->size].item);
			}
			free((*h)->heap);
		}
		free(*h);
		*h = NULL;
	}
}

unsigned long int heap_size(heap const *restrict h) {
	if (h != NULL) {
		return h->size;
	}
	return 0;
}

#if HEAP_DEBUG == 1
	int main(int argc, char *argv[]) {
		heap *h = heap_start();

		int *item;
		float key = 1;
		for (int i = 0; i < 6; i++) {
			item = malloc(sizeof(int));
			*item = i * i;
			key = key * (-0.5) * (float) (1 + i);
			heap_push(h, key, item);
			printf("pushed (%f, %d)\n", key, *item);
		}

		for (int i = 0; i < 6; i++)
			printf("[%d, %d]. (%f, %d)\n", HEAP_MASTER(i), i, 
				h->heap[i].key, *(int *)h->heap[i].item);

		for (int i =0; i < 6; i++) {
			item = heap_pop(h);
			printf("pop: %d\n", *item);
			free(item);
		}

		heap_destroy(&h);

		return 0;
	}
#endif
