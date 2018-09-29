#ifndef __HEAP_H__
#define __HEAP_H__

#define HEAP_LCHILD(NODE) (1 + (NODE) * 2)
#define HEAP_RCHILD(NODE) (2 + (NODE) * 2)
#define HEAP_MASTER(NODE) (((NODE) > 0) ? (((NODE) - 1) / 2) : 0)

#ifndef MIN
	#define MIN(A,B) (((A) < (B)) ? (A) : (B))
#endif

#define HEAP_KEY(NODE) (*(float *)(NODE))

typedef struct heap_struct heap;

heap *heap_start();
void *heap_pop(heap *restrict h);
void heap_push(heap *h, unsigned char *restrict key_and_move);
void heap_destroy(heap **h);
unsigned long int heap_size(heap const *restrict h);

#endif
