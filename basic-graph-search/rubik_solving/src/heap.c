#include <stdlib.h>
#include <stdio.h>
#include <heap.h>

#define HEAP_DEBUG 0

#if ENABLE_IDA_STAR
	typedef struct {
		void *item;
		float key;
	} heap_node;

	#ifdef IN_STACK_WE_TRUST
		#define HEAP_INIT_BUFFER_SIZE (12 * sizeof(heap_node))
	#endif

	struct heap_struct {
		#ifdef IN_STACK_WE_TRUST
			heap_node heap[HEAP_INIT_BUFFER_SIZE];
		#else
			heap_node ** restrict heap;
			unsigned long int buffer_size;
		#endif
		unsigned long int size;
	};
#else
	struct heap_struct {
		unsigned char ** restrict heap;
		unsigned long int buffer_size;
		unsigned long int size;
	};
#endif

heap *heap_start() {
	heap *h = malloc(sizeof(heap));
	if (h != NULL) {
		#ifndef IN_STACK_WE_TRUST
			h->heap = malloc(sizeof(
			#if ENABLE_IDA_STAR
				heap_node
			#else
				unsigned char *
			#endif
				) * HEAP_INIT_BUFFER_SIZE);

			h->buffer_size = HEAP_INIT_BUFFER_SIZE;
		#endif
		h->size = 0;
	}
	return h;
}

void *heap_pop(heap *h) {
	item_type *item = HEAP_HEAD_ITEM(h);

	register unsigned long cur_position = 0, min_index,
		lchild_index = HEAP_LCHILD(cur_position), 
		rchild_index = HEAP_RCHILD(cur_position);
	register const unsigned long cur_size = --h->size;

	#ifndef IN_STACK_WE_TRUST
		#if ENABLE_IDA_STAR
			void *
		#else
			unsigned char *
		#endif
	#else
		heap_node
	#endif
		aux;

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

	#ifndef IN_STACK_WE_TRUST
		#if ENABLE_IDA_STAR
			free(h->heap[cur_size]);
		#endif
	#endif

	return item;
}

void heap_push(heap *h, 
	#if ENABLE_IDA_STAR
		void *restrict item,
		float const key
	#else
		unsigned char *restrict key_and_move
	#endif
	) {

	register const unsigned long int cur_size = h->size;
	register unsigned long int cur_position = cur_size;

	#ifdef IN_STACK_WE_TRUST
		h->heap[cur_size].item = item;
		h->heap[cur_size].key = key;
	#else
		#if ENABLE_IDA_STAR == 0
			// If ENABLE_IDA_STAR is enabled, then the initial
			// HEAP BUFFER must be fixed.
			if (cur_size + 1 >= h->buffer_size) {
				h->buffer_size *= 2;
				h->heap = realloc(h->heap, sizeof(unsigned char *) * h->buffer_size);
			}

			h->heap[cur_size] = key_and_move;
		#else 
			heap_node *hn = malloc(sizeof(heap_node));
			hn->item = item;
			hn->key = key;
			h->heap[cur_size] = hn;
		#endif
	#endif

	#ifndef IN_STACK_WE_TRUST
		#if ENABLE_IDA_STAR
			register heap_node
				**master_node = h->heap + HEAP_MASTER(cur_position), 
				**cur_node = h->heap + cur_position, *aux;
		#else
			register unsigned char
				**master_node = h->heap + HEAP_MASTER(cur_position), 
				**cur_node = h->heap + cur_position, *aux;
		#endif
	#else
		register heap_node
			*master_node = h->heap + HEAP_MASTER(cur_position), 
			*cur_node = h->heap + cur_position, aux;
	#endif

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
		#ifndef IN_STACK_WE_TRUST
			if ((*h)->heap != NULL) {
				free((*h)->heap);
			}
		#endif
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

void heap_conditional_purge(heap *h) {
	if (heap_size(h) > MAX_HEAP_SIZE) {
		for (unsigned long i = KEEP_BEST_UNTIL; i < h->size; i++) {
			free(h->heap[i]);
		}
		// Not necessary do adjust memory, as it would
		// only slow down the insert process
		h->size = KEEP_BEST_UNTIL;
	}
}

#if HEAP_DEBUG == 1
	int main(int argc, char *argv[]) {
		heap *h = heap_start();

		unsigned char *item;
		for (int i = 0; i < 6; i++) {
			item = malloc(2*sizeof(unsigned char));
			item[0] = rand();
			item[1] = i * i;
			#if ENABLE_IDA_STAR
				heap_push(h, item, *item);
			#else
				heap_push(h, item);
			#endif
			printf("pushed (%d, %d)\n", item[0], item[1]);
		}

		for (int i = 0; i < 6; i++)
			#if ENABLE_IDA_STAR
				printf("[%d, %d]. (%f, %d)\n", HEAP_MASTER(i), i,
					HEAP_KEY(h->heap[i]), ((int *)h->heap[i]->item)[1]);
			#else
				printf("[%d, %d]. (%d, %d)\n", HEAP_MASTER(i), i,
					HEAP_KEY(h->heap[i]), h->heap[i][0]);
			#endif

		for (int i =0; i < 6; i++) {
			item = heap_pop(h);
			printf("pop: %d\n", *item);
			free(item);
		}

		heap_destroy(&h);

		return 0;
	}
#endif
