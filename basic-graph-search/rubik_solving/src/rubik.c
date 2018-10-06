#include <stdlib.h>
#include <stdio.h>
#include <rubik.h>
#include <string.h>
#include <heap.h>

#if ENABLE_IDA_STAR
	#include <stack.h>
#endif

struct rubik_struct {
	color_type config[COLOR_NUM][ROW_NUM][COL_NUM],
		INITIAL_CONFIG[COLOR_NUM][ROW_NUM][COL_NUM],
		*p_c[COLOR_NUM][ROW_NUM + 2][COL_NUM + 2],
		aux_p_c[ROW_NUM + 2][COL_NUM + 2];
	unsigned char sol_size, *solution, nil_pos;
};

#if ENABLE_IDA_STAR
	typedef struct {
		unsigned char *cur_moves;
		color_type cur_config[COLOR_NUM][ROW_NUM][COL_NUM];
	} package;
#endif

enum {
	#if ENABLE_IDA_STAR
		PACK_GCOST,

	#else
		PACK_HEAPKEY,
		PACK_GCOST=sizeof(float),
	#endif
	PACK_MOVES,
	PACK_SIZE
};

static void __attribute__((cold)) __build_pointer_matrix__(rubik *restrict r) {

	color_type *p_G_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{&r->nil_pos, &r->config[C_W][0][0], &r->config[C_W][0][1], &r->config[C_W][0][2], &r->nil_pos},
		{&r->config[C_O][2][0], &r->config[C_G][0][0], &r->config[C_G][1][0], &r->config[C_G][2][0], &r->config[C_R][0][0]},
		{&r->config[C_O][2][1], &r->config[C_G][0][1], &r->config[C_G][1][1], &r->config[C_G][2][1], &r->config[C_R][0][1]},
		{&r->config[C_O][2][2], &r->config[C_G][0][2], &r->config[C_G][1][2], &r->config[C_G][2][2], &r->config[C_R][0][2]},
		{&r->nil_pos, &r->config[C_Y][0][2], &r->config[C_Y][0][1], &r->config[C_Y][0][0], &r->nil_pos},
	};

	color_type *p_O_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{&r->nil_pos, &r->config[C_W][2][0], &r->config[C_W][1][0], &r->config[C_W][0][0], &r->nil_pos},
		{&r->config[C_B][2][0], &r->config[C_O][0][0], &r->config[C_O][1][0], &r->config[C_O][2][0], &r->config[C_G][0][0]},
		{&r->config[C_B][2][1], &r->config[C_O][0][1], &r->config[C_O][1][1], &r->config[C_O][2][1], &r->config[C_G][0][1]},
		{&r->config[C_B][2][2], &r->config[C_O][0][2], &r->config[C_O][1][2], &r->config[C_O][2][2], &r->config[C_G][0][2]},
		{&r->nil_pos, &r->config[C_Y][0][2], &r->config[C_Y][1][2], &r->config[C_Y][2][2], &r->nil_pos},
	};

	color_type *p_B_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{&r->nil_pos, &r->config[C_W][2][2], &r->config[C_W][2][1], &r->config[C_W][2][0], &r->nil_pos},
		{&r->config[C_R][2][0], &r->config[C_B][0][0], &r->config[C_B][1][0], &r->config[C_B][2][0], &r->config[C_O][0][0]},
		{&r->config[C_R][2][1], &r->config[C_B][0][1], &r->config[C_B][1][1], &r->config[C_B][2][1], &r->config[C_O][0][1]},
		{&r->config[C_R][2][2], &r->config[C_B][0][2], &r->config[C_B][1][2], &r->config[C_B][2][2], &r->config[C_O][0][2]},
		{&r->nil_pos, &r->config[C_Y][2][0], &r->config[C_Y][2][1], &r->config[C_Y][2][2], &r->nil_pos},
	};

	color_type *p_Y_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{&r->nil_pos, &r->config[C_R][0][2], &r->config[C_R][1][2], &r->config[C_R][2][2], &r->nil_pos},
		{&r->config[C_G][2][2], &r->config[C_Y][0][0], &r->config[C_Y][1][0], &r->config[C_Y][2][0], &r->config[C_B][0][2]},
		{&r->config[C_G][1][2], &r->config[C_Y][0][1], &r->config[C_Y][1][1], &r->config[C_Y][2][1], &r->config[C_B][1][2]},
		{&r->config[C_G][0][2], &r->config[C_Y][0][2], &r->config[C_Y][1][2], &r->config[C_Y][2][2], &r->config[C_B][2][2]},
		{&r->nil_pos, &r->config[C_O][2][2], &r->config[C_O][1][2], &r->config[C_O][0][2], &r->nil_pos},
	};

	color_type *p_R_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{&r->nil_pos, &r->config[C_W][0][2], &r->config[C_W][1][2], &r->config[C_W][2][2], &r->nil_pos},
		{&r->config[C_G][2][0], &r->config[C_R][0][0], &r->config[C_R][1][0], &r->config[C_R][2][0], &r->config[C_B][0][0]},
		{&r->config[C_G][2][1], &r->config[C_R][0][1], &r->config[C_R][1][1], &r->config[C_R][2][1], &r->config[C_B][0][1]},
		{&r->config[C_G][2][2], &r->config[C_R][0][2], &r->config[C_R][1][2], &r->config[C_R][2][2], &r->config[C_B][0][2]},
		{&r->nil_pos, &r->config[C_Y][0][0], &r->config[C_Y][1][0], &r->config[C_Y][2][0], &r->nil_pos},
	};

	color_type *p_W_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{&r->nil_pos, &r->config[C_O][2][0], &r->config[C_O][1][0], &r->config[C_O][0][0], &r->nil_pos},
		{&r->config[C_G][0][0], &r->config[C_W][0][0], &r->config[C_W][1][0], &r->config[C_W][2][0], &r->config[C_B][2][0]},
		{&r->config[C_G][1][0], &r->config[C_W][0][1], &r->config[C_W][1][1], &r->config[C_W][2][1], &r->config[C_B][1][0]},
		{&r->config[C_G][2][0], &r->config[C_W][0][2], &r->config[C_W][1][2], &r->config[C_W][2][2], &r->config[C_B][0][0]},
		{&r->nil_pos, &r->config[C_R][0][0], &r->config[C_R][1][0], &r->config[C_R][2][0], &r->nil_pos},
	};

	memcpy(r->p_c[C_W], p_W_mat, sizeof(p_W_mat));
	memcpy(r->p_c[C_Y], p_Y_mat, sizeof(p_Y_mat));
	memcpy(r->p_c[C_G], p_G_mat, sizeof(p_G_mat));
	memcpy(r->p_c[C_R], p_R_mat, sizeof(p_R_mat));
	memcpy(r->p_c[C_B], p_B_mat, sizeof(p_B_mat));
	memcpy(r->p_c[C_O], p_O_mat, sizeof(p_O_mat));
}

inline static float __attribute__((hot, pure)) __heuristic_cost__(rubik const *const restrict r) {
	float h_cost = 0.0;

	unsigned char color, row, col;
	register unsigned char cur_pos_color;
	for (color = 0; color < COLOR_NUM; color++) {
		for (row = 0; row < ROW_NUM; row++) {
			for (col = 0; col < COL_NUM; col++) {
				cur_pos_color = r->config[color][row][col];
				h_cost += (cur_pos_color != COLOR_SEQ[color]) + 
					OPPOSITE_COLORS(cur_pos_color, color);
			}
		}
	}
	// This is roughly an division by 12
	return h_cost * 0.083334;
}

static void __attribute__((hot, nonnull)) 
	__mat_rot__(
	rubik *restrict r, 
	unsigned char color_id, 
	unsigned char clockwise,
	char times) {

	unsigned char row, col;
	while (times-- > 0) {
		for (row = 0; row < ROW_NUM + 2; row++) {
			for (col = 0; col < COL_NUM + 2; col++) {
				if (clockwise == DIR_CLKWISE) {
					r->aux_p_c[row][4 - col] = *r->p_c[color_id][col][row];
				} else {
					r->aux_p_c[4 - row][col] = *r->p_c[color_id][col][row];
				}
			}
		}

		for (row = 0; row < ROW_NUM + 2; row++) {
			for (col = 0; col < COL_NUM + 2; col++) {
				*r->p_c[color_id][row][col] = r->aux_p_c[row][col];
			}
		}
	}
}

static inline void __attribute__((hot, nonnull)) 
	__recover_state__(
	rubik *restrict r, 
	unsigned char const *restrict const moves) {
	
	// Recover initial position	
	memcpy(r->config, r->INITIAL_CONFIG, sizeof(r->INITIAL_CONFIG));

	// Redo all moves through current state
	unsigned char color, clockwise;
	const unsigned char moves_count = moves[PACK_GCOST] + PACK_MOVES;
	for (register size_t i = PACK_MOVES; i < moves_count; i++) {
		color = moves[i] & MASK_COL;
		clockwise = moves[i] & MASK_DIR;
		__mat_rot__(r, color, clockwise, 1);
	}
}

rubik * __attribute__((cold)) rubik_create(char *const restrict filepath) {
	rubik *r = NULL;

	FILE *restrict input_f = fopen(filepath, "r");
	
	if (input_f != NULL) {
		register unsigned char color, row, col;

		// Allocate rubik's cube structure
		r = malloc(sizeof(rubik));

		if (r != NULL) {
			r->sol_size = 0;
			r->solution = NULL;

			for (color = 0; color < COLOR_NUM; color++)
				for (row = 0; row < ROW_NUM; row++)
					for (col = 0; col < COL_NUM && 
						fscanf(input_f, "%c%*c", &r->config[color][row][col]); col++);
		}

		fclose(input_f);

		// Store a copy of the initial configuration
		memcpy(r->INITIAL_CONFIG, r->config, sizeof(r->config));

		// Build up pointer matrices
		__build_pointer_matrix__(r);
	} 

	return r;
}

int __attribute__((cold)) rubik_print(const rubik *const restrict r) {
	if (r != NULL) {

		register unsigned char i, row = 0, col = 0, color;

		const char offset[] = "      ";
		for (i = 0; i < sizeof(PRINT_COLOR_SEQ)/sizeof(char)-1; i++) {
			color = (int) PRINT_COLOR_SEQ[i] - (int) '0';
			printf("%s", (color == C_W || color == C_Y) ? offset : ""); 
			for (row = 0; row < ROW_NUM; row++) {
				printf("%c ", r->config[color][row][col]);
			}
			printf("%c", PRINT_BREAKLINE[i]);
			col = (col + (PRINT_BREAKLINE[i] == '\n')) % COL_NUM;
		}
		printf("\n");
		return 1;
	}
	return 0;
}

static 
#if ENABLE_IDA_STAR
	package * __attribute__((hot))
	__empty_move__(const rubik * restrict const r) {
#else
	unsigned char *	__attribute__((cold))
	__empty_move__() {
#endif

	#if ENABLE_IDA_STAR
		package *new_item = malloc(sizeof(package));
		memcpy(new_item->cur_config, r->INITIAL_CONFIG, sizeof(r->INITIAL_CONFIG));
		new_item->cur_moves = malloc(PACK_SIZE * sizeof(unsigned char));
		new_item->cur_moves[PACK_GCOST] = 0;
		new_item->cur_moves[PACK_MOVES] = '\0';
	#else
		unsigned char *new_item = malloc(PACK_SIZE * sizeof(unsigned char));
		new_item[PACK_HEAPKEY] = 0.0;
		new_item[PACK_GCOST] = 0;
		new_item[PACK_MOVES] = '\0';

	#endif

	return new_item;
}

int __attribute__((hot)) rubik_solve(rubik *restrict r) {
	if (r != NULL) {
		const unsigned char __attribute__((aligned(__BIGGEST_ALIGNMENT__))) 
			DIR_SEQ[] = {DIR_CLKWISE, DIR_C_CLKWISE, DIR_CLKWISE};
		register float new_heuristic_cost;

		#if ENABLE_IDA_STAR
			package *cur_item_package,
				*new_item_package = __empty_move__(r);
			register unsigned char *cur_item, *new_item; 
		#else 
			register unsigned char *cur_item, 
				*new_item = __empty_move__(); 
			float *aux_h_pointer;
		#endif

		register unsigned char 
			not_completed = 1, 
			color, 
			dir;

		heap *minheap = heap_start();

		#if ENABLE_IDA_STAR
			stack *movestack = stack_start();
			stack_push(movestack, new_item_package);
			register float threshold = __heuristic_cost__(r), 
				next_threshold = threshold;
			float f_cost_total;
		#else
			aux_h_pointer = (float *) new_item;
			aux_h_pointer[PACK_HEAPKEY] = 0.0;
			heap_push(minheap, new_item);
		#endif

		if (
		#if ENABLE_IDA_STAR
			threshold
		#else
			__heuristic_cost__(r) 
		#endif
			<= 0.0) not_completed = 0;

		while (not_completed) {
			#if ENABLE_IDA_STAR
				/*
					IDA* is a IDDFS algorthm which uses the
					"maximum deep" as some threshold for the
					f_cost function of A*.
				*/
				if (stack_not_empty(movestack)) {
					cur_item_package = stack_pop(movestack);
				} else {
					// Next IDDFS algorithm: init a empty
					// move and update threshold
					cur_item_package = __empty_move__(r);
					threshold = next_threshold + IDA_DEGREES_OF_FREEDOM;
					next_threshold = INFINITY;
				}

				cur_item = cur_item_package->cur_moves;

				// IDA* is memory constrained so it can happily
				// keep a entire copy of the cube in item structure.
				memcpy(r->config, cur_item_package->cur_config, sizeof(r->config));
				free(cur_item_package);
			#else
				cur_item = heap_pop(minheap);

				// Recover the configuration of popped snapshot
				__recover_state__(r, cur_item);
			
			#endif

			for (color = 0; (color < COLOR_NUM) && not_completed; color++) {
				for (dir = 0; (dir < 2) && not_completed; dir++) {
					__mat_rot__(r, color, DIR_SEQ[dir], 1);
					new_heuristic_cost = __heuristic_cost__(r);
					not_completed &= (new_heuristic_cost > 0.0);

					#if ENABLE_IDA_STAR
						f_cost_total = new_heuristic_cost + cur_item[PACK_GCOST] + 1; 
						if (f_cost_total <= threshold) {
					#endif

					new_item = malloc(sizeof(unsigned char) * (PACK_SIZE + cur_item[PACK_GCOST]));
					new_item[PACK_GCOST] = cur_item[PACK_GCOST] + 1;
					memcpy(new_item + PACK_MOVES, cur_item + PACK_MOVES, cur_item[PACK_GCOST]);
					new_item[PACK_MOVES + cur_item[PACK_GCOST]] = color | DIR_SEQ[dir];

					#if ENABLE_IDA_STAR == 0
						aux_h_pointer = (float *) new_item;
						aux_h_pointer[PACK_HEAPKEY] = new_heuristic_cost + new_item[PACK_GCOST];
					#endif
					
					#if ENABLE_IDA_STAR
						// Turn minheap into maxheap reversing the key signal
						f_cost_total *= -1.0;

						new_item_package = malloc(sizeof(package));
						new_item_package->cur_moves = new_item;
						memcpy(new_item_package->cur_config, r->config, sizeof(r->config));
		
						heap_push(minheap, new_item_package, f_cost_total);

						} else {
							next_threshold = MIN(next_threshold, f_cost_total);
						}
					#else
						heap_push(minheap, new_item);
					#endif

					// Recover previous state
					__mat_rot__(r, color, DIR_SEQ[dir + 1], 1);
				} // End of DIR loop
			} // End of COLOR loop

			#if ENABLE_IDA_STAR
				// Heapsort on movement stack
				color = heap_size(minheap);
				while (color--) {
					stack_push(movestack, heap_pop(minheap));
				}
			#endif

			free(cur_item);
		}

		#if ENABLE_IDA_STAR
			cur_item_package = stack_pop(movestack);
			cur_item = cur_item_package->cur_moves;
			memcpy(r->config, cur_item_package->cur_config, sizeof(r->config));
			free(cur_item_package);
		#else
			cur_item = heap_pop(minheap);
			__recover_state__(r, cur_item);
		#endif

		r->sol_size = cur_item[PACK_GCOST];
		r->solution = malloc(sizeof(unsigned char) * r->sol_size);
		memcpy(r->solution, cur_item + PACK_MOVES, r->sol_size);
		free(cur_item);

		#if ENABLE_IDA_STAR
			while (stack_not_empty(movestack)) {
				new_item_package = stack_pop(movestack);
				free(new_item_package->cur_moves);
				free(new_item_package);
			}
		#else
			for (register unsigned long i = heap_size(minheap); i; i--) {
				new_item = heap_pop(minheap);
				free(new_item);
			}
		#endif

		#if ENABLE_IDA_STAR
			stack_destroy(&movestack);
		#endif

		heap_destroy(&minheap);

		return 1;
	}
	return 0;
}

int __attribute__((cold)) rubik_solution(const rubik *const restrict r) {
	if (r != NULL) {
		unsigned char col, dir;
		for (register unsigned char i = 0; i < r->sol_size; i++) {
			col = COLOR_SEQ[r->solution[i] & MASK_COL];
			dir = r->solution[i] & MASK_DIR;
			printf("%hhu\t: %c %s\n", i + 1, col,
				dir == DIR_CLKWISE ? "->" : "<-");
		}

		return 1;
	}
	return 0;
}

int __attribute__((cold)) rubik_destroy(rubik **restrict r) {
	if (r != NULL && *r != NULL) {
		if ((*r)->solution)
			free((*r)->solution);
		free(*r);
		*r = NULL;
		return 1;
	}
	return 0;
}

int __attribute__((cold)) rubik_reinit(rubik *restrict r) {
	if (r != NULL) {
		return (memcpy(r->INITIAL_CONFIG, 
			r->config, sizeof(r->config)) != NULL);
	}
	return 0;
}

int __attribute__((cold)) rubik_rotate(rubik *restrict r, 
	unsigned char const color, 
	unsigned char const clockwise) {

	if (r != NULL) {
		__mat_rot__(r, color, clockwise, 1);
		return 1;
	}
	return 0;
}
