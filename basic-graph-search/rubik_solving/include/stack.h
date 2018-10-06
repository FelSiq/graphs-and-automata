#ifndef __STACK_H__
#define __STACK_H__

#ifndef IN_STACK_WE_TRUST
	#define STACK_INIT_BUFFER_SIZE 4096
#else
	#include <rubik.h>
	#define STACK_INIT_BUFFER_SIZE (12 * 26 * (COLOR_NUM) * (COL_NUM) * (ROW_NUM))
#endif

typedef struct stack_struct stack;

stack *stack_start();
void *stack_pop(stack *restrict s);
void stack_push(stack *s, void *restrict move);
void stack_destroy(stack **s);
unsigned long int stack_not_empty(stack const *restrict s);

#endif
