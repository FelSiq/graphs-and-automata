#include <stdlib.h>
#include <stdio.h>
#include <heap.h>

#define HEAP_DEBUG 0

struct heap_struct {
	unsigned char ** restrict heap;
	unsigned long int buffer_size;
	unsigned long int size;
};

heap *heap_start() {
	heap *h = malloc(sizeof(heap));
	if (h != NULL) {
		h->heap = malloc(sizeof(unsigned char *) * HEAP_INIT_BUFFER_SIZE);
		h->buffer_size = HEAP_INIT_BUFFER_SIZE;
		h->size = 0;
	}
	return h;
}

void *heap_pop(heap *h) {
	unsigned char *item = h->heap[0];

	register unsigned long cur_position = 0, min_index,
		lchild_index = HEAP_LCHILD(cur_position), 
		rchild_index = HEAP_RCHILD(cur_position);
	register const unsigned long cur_size = --h->size;

	unsigned char *aux;

	// Swap head node with tail node
	aux = h->heap[0];
	h->heap[0] = h->heap[cur_size];
	h->heap[cur_size] = aux;

	// Downgrade "new head node" to its respective place
	while (lchild_index < cur_size) {

		if (rchild_index < cur_size && 
			HEAP_KEY(h->heap[rchild_index]) < HEAP_KEY(h->heap[lchild_index])) {
			min_index = rchild_index;
		} else {
			min_index = lchild_index;
		}

		if (HEAP_KEY(h->heap[min_index]) < HEAP_KEY(h->heap[cur_position])) {
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

void heap_push(heap *h, unsigned char *restrict key_and_move) {
	register const unsigned long int cur_size = h->size;
	register unsigned long int cur_position = cur_size;

	#if ENABLE_IDA_STAR == 0
		// If ENABLE_IDA_STAR is enabled, then the initial
		// HEAP BUFFER must be fixed.
		if (cur_size + 1 >= h->buffer_size) {
			h->buffer_size *= 2;
			h->heap = realloc(h->heap, sizeof(unsigned char *) * h->buffer_size);
		}
	#endif

	h->heap[cur_size] = key_and_move;

	unsigned char *aux;
	register unsigned char
		**master_node = h->heap + HEAP_MASTER(cur_position), 
		**cur_node = h->heap + cur_position;

	while (HEAP_KEY(*master_node) > HEAP_KEY(*cur_node)) {
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

		unsigned char *item;
		for (int i = 0; i < 6; i++) {
			item = malloc(2*sizeof(unsigned char));
			item[0] = rand();
			item[1] = i * i;
			heap_push(h, item);
			printf("pushed (%d, %d)\n", item[0], item[1]);
		}

		for (int i = 0; i < 6; i++)
			printf("[%d, %d]. (%d, %d)\n", HEAP_MASTER(i), i,
				HEAP_KEY(h->heap[i]), h->heap[i][1]);

		for (int i =0; i < 6; i++) {
			item = heap_pop(h);
			printf("pop: %d\n", *item);
			free(item);
		}

		heap_destroy(&h);

		return 0;
	}
#endif
