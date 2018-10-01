#ifndef __STACK_H__
#define __STACK_H__

#define STACK_INIT_BUFFER_SIZE 4096

typedef struct stack_struct stack;

stack *stack_start();
void *stack_pop(stack *restrict s);
void stack_push(stack *s, unsigned char *restrict move);
void stack_destroy(stack **s);
unsigned long int stack_not_empty(stack const *restrict s);

#endif
