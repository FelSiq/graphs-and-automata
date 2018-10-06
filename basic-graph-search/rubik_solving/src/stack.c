#include <stdlib.h>
#include <stdio.h>
#include <stack.h>

#define STACK_DEBUG 0

struct stack_struct {
	#ifdef IN_STACK_WE_TRUST
		void *restrict stack[STACK_INIT_BUFFER_SIZE];
	#else
		void ** restrict stack;
		unsigned long int buffer_size;
	#endif

	unsigned long int size;
};


stack *stack_start() {
	stack *s = malloc(sizeof(stack));
	if (s != NULL) {
		#ifndef IN_STACK_WE_TRUST
			s->stack = malloc(sizeof(void *) * STACK_INIT_BUFFER_SIZE);
			s->buffer_size = STACK_INIT_BUFFER_SIZE;
		#endif
		s->size = 0;
	}
	return s;
}

void *stack_pop(stack *s) {
	return s->stack[--s->size];
}

void stack_push(stack *s, void * restrict move) {
	register const unsigned long int cur_size = ++s->size;
	#ifndef IN_STACK_WE_TRUST
	if (cur_size >= s->buffer_size) {
		s->buffer_size *= 2;
		s->stack = realloc(s->stack, sizeof(void *) * s->buffer_size);
	}
	#endif
	s->stack[cur_size - 1] = move;
}

void stack_destroy(stack **s) {
	if (s != NULL && *s != NULL) {
		#ifndef IN_STACK_WE_TRUST
		if ((*s)->stack != NULL) {
			free((*s)->stack);
		}
		#endif
		free(*s);
		*s = NULL;
	}
}

unsigned long int stack_not_empty(stack const *restrict s) {
	if (s != NULL) {
		return s->size > 0;
	}
	return 0;
}

#if STACK_DEBUG == 1
	#define STACK_DEBUG_LOOP_SIZE 10
	int main(int argc, char *argv[]) {
		stack *s = stack_start();

		unsigned char *item;
		for (int i = 0; i < STACK_DEBUG_LOOP_SIZE; i++) {
			item = malloc(2*sizeof(unsigned char));
			item[0] = rand();
			item[1] = i * i;
			stack_push(s, item);
			printf("pushed (%d, %d)\n", item[0], item[1]);
		}

		for (int i =0; i < STACK_DEBUG_LOOP_SIZE; i++) {
			item = stack_pop(s);
			printf("pop: %d\n", *item);
			free(item);
		}

		stack_destroy(&s);

		return 0;
	}
#endif
