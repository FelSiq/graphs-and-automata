#ifndef __HEAP_H__
#define __HEAP_H__

#define CONSTRAINT_HEAP_SIZE 1
#define MAX_HEAP_SIZE ((unsigned int) (5e+7))
#define KEEP_BEST_UNTIL ((unsigned int) (2e+7))

#define HEAP_LCHILD(NODE) (1 + (NODE) * 2)
#define HEAP_RCHILD(NODE) (2 + (NODE) * 2)
#define HEAP_MASTER(NODE) (((NODE) > 0) ? (((NODE) - 1) / 2) : 0)

#ifndef IN_STACK_WE_TRUST
	#define HEAP_INIT_BUFFER_SIZE (12 * sizeof(unsigned char *))
#endif

#ifndef MIN
	#define MIN(A,B) (((A) < (B)) ? (A) : (B))
#endif

#if ENABLE_IDA_STAR
	#ifndef IN_STACK_WE_TRUST
		#define HEAP_KEY(NODE) ((NODE)->key)
		#define HEAP_HEAD_ITEM(HEAP_STR) ((HEAP_STR)->heap[0]->item)
	#else
		#define HEAP_KEY(NODE) ((NODE).key)
		#define HEAP_HEAD_ITEM(HEAP_STR) ((HEAP_STR)->heap[0].item)
	#endif
	typedef void * item_type;
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
void heap_conditional_purge(heap *h);

#endif
