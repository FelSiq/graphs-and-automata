#ifndef __HEAP_H__
#define __HEAP_H__

#define HEAP_LCHILD(NODE) (1 + (NODE) * 2)
#define HEAP_RCHILD(NODE) (2 + (NODE) * 2)
#define HEAP_MASTER(NODE) (((NODE) > 0) ? (((NODE) - 1) / 2) : 0)

#define HEAP_INIT_BUFFER_SIZE (12 * sizeof(unsigned char *))

#ifndef MIN
	#define MIN(A,B) (((A) < (B)) ? (A) : (B))
#endif

#if ENABLE_IDA_STAR
	#define HEAP_KEY(NODE) ((NODE)->key)
	#define HEAP_HEAD_ITEM(HEAP_STR) ((HEAP_STR)->heap[0]->item)
	typedef void *item_type;
#else
	#define HEAP_KEY(NODE) (*(float *)(NODE))
	#define HEAP_HEAD_ITEM(HEAP_STR) ((HEAP_STR)->heap[0])
	typedef unsigned char item_type;
#endif

typedef struct heap_struct heap;

heap *heap_start();
void *heap_pop(heap *restrict h);
void heap_push(heap *h, 
#if ENABLE_IDA_STAR
	void *restrict item,
	float const key
#else
	unsigned char *restrict key_and_move
#endif
);

void heap_destroy(heap **h);
unsigned long int heap_size(heap const *restrict h);

#endif
