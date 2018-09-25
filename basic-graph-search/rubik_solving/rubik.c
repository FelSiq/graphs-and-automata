#include <stdlib.h>
#include <stdio.h>
#include <rubik.h>
#include <string.h>
#include <heap.h>

struct rubik_struct {
	color_type config[COLOR_NUM][ROW_NUM][COL_NUM],
		INITIAL_CONFIG[COLOR_NUM][ROW_NUM][COL_NUM],
		*p_c[COLOR_NUM][ROW_NUM + 2][COL_NUM + 2],
		aux_p_c[ROW_NUM + 2][COL_NUM + 2];
	unsigned char sol_size, *solution, nil_pos;
};

typedef struct {
	float hcost;
	unsigned char gcost;
	unsigned char *moves;
} package;

static void __build_pointer_matrix__(rubik *restrict r) {

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

inline static float __heuristic_cost__(rubik const *const restrict r) {
	float h_cost = 0.0;

	unsigned char color, row, col;
	for (color = 0; color < COLOR_NUM; color++)
		for (row = 0; row < ROW_NUM; row++)
			for (col = 0; col < COL_NUM; col++)
				h_cost += r->config[color][row][col] != COLOR_SEQ[color];

	// This is roughly an division by 12
	return h_cost * 0.0834;
}

static void __mat_rot__(
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

#if DEBUG == 1
	static void __print_pointer_mat__(color_type *mat[5][5]) {
		for (int row = 0; row < 5; row++){
			for (int col = 0; col < 5; col++) {
				printf("%c ", *mat[row][col]);
			}
			printf("\n");
		}
	}

	static void __rotation_test__(rubik *r) {
		for (unsigned char color = 0; color < COLOR_NUM; color++) {
			printf("Color: %d\n", color);
			__print_pointer_mat__(r->p_c[color]);
			for (unsigned char i = 0; i < 4; i++) {
				printf("Rotation -> %d:\n", i+1);
				__mat_rot__(r, color, DIR_CLKWISE, 1);
				__print_pointer_mat__(r->p_c[color]);
			}
			for (unsigned char i = 0; i < 4; i++) {
				printf("Rotation <- %d:\n", i+1);
				__mat_rot__(r, color, DIR_C_CLKWISE, 1);
				__print_pointer_mat__(r->p_c[color]);
			}
			printf("After all rotations:\n");
			__print_pointer_mat__(r->p_c[color]);
			printf("End of color %d\n", color);
		}
	}
#endif

rubik *rubik_create(char *const restrict filepath) {
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
					for (col = 0; col < COL_NUM; col++)
						fscanf(input_f, "%c%*c", &r->config[color][row][col]);
		}

		fclose(input_f);

		// Store a copy of the initial configuration
		memcpy(r->INITIAL_CONFIG, r->config, sizeof(r->config));

		// Build up pointer matrices
		__build_pointer_matrix__(r);
	} 

	#if DEBUG == 1
		__rotation_test__(r);
	#endif
	__mat_rot__(r, C_R, DIR_C_CLKWISE, 1);
	__mat_rot__(r, C_W, DIR_C_CLKWISE, 1);

	return r;
}

int rubik_print(const rubik *const restrict r) {
	if (r != NULL) {

		register unsigned char i, row = 0, col, color;

		const char offset[] = "      ";
		for (i = 0; i < sizeof(PRINT_COLOR_SEQ)/sizeof(char); i++) {
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

static void __recover_state__(const rubik *restrict r, 
	unsigned char const *restrict const moves) {

}

int rubik_solve(rubik *restrict r) {
	if (r == NULL) {
		register package *cur_item, *new_item;
		heap *minheap = heap_start();

		register unsigned char not_completed = 1, color;
		while (not_completed) {
			cur_item = heap_pop(minheap);
			// Recover the configuration of popped snapshot
			__recover_state__(r, cur_item->moves);
			
			if (cur_item->hcost > 0.0) {
				for (color = 0; color < COLOR_NUM; color++) {
					// Clockwise movements
					__mat_rot__(r, color, DIR_CLKWISE, 1);
					new_item = malloc(sizeof(package));
					new_item->hcost = __heuristic_cost__(r);
					new_item->gcost = cur_item->gcost + 1;
					new_item->moves = malloc(sizeof(char) * new_item->gcost);
					memcpy(new_item->moves, cur_item->moves, cur_item->gcost);
					new_item->moves[new_item->gcost - 1] = color & DIR_CLKWISE;
					heap_push(minheap, new_item->hcost + new_item->gcost, new_item);

					// Counter-clockwise movements
					__mat_rot__(r, color, DIR_C_CLKWISE, 2);
					new_item = malloc(sizeof(package));
					new_item->hcost = __heuristic_cost__(r);
					new_item->gcost = cur_item->gcost + 1;
					new_item->moves = malloc(sizeof(char) * new_item->gcost);
					memcpy(new_item->moves, cur_item->moves, cur_item->gcost);
					new_item->moves[new_item->gcost - 1] = color & DIR_C_CLKWISE;
					heap_push(minheap, new_item->hcost + new_item->gcost, new_item);

					// Recover previous state
					__mat_rot__(r, color, DIR_CLKWISE, 1);
				}

			} else {
				not_completed = 0;
				r->solution = cur_item->moves;
				r->sol_size = strlen((char *) cur_item->moves);
			}

			free(cur_item);
		}

		heap_destroy(&minheap);
		return 1;
	}
	return 0;
}

int rubik_solution(const rubik *const restrict r) {
	if (r != NULL) {
		unsigned char col, dir;
		for (register unsigned char i = 0; i < r->sol_size; i++) {
			col = COLOR_SEQ[r->solution[i] & MASK_COL];
			dir = r->solution[i] & MASK_DIR;
			printf("%hhu\t: %hhu %s", i, col,
				dir == DIR_CLKWISE ? "->" : "<-");
		}

		return 1;
	}
	return 0;
}

int rubik_destroy(rubik **restrict r) {
	if (r != NULL && *r != NULL) {
		free(*r);
		*r = NULL;
		return 1;
	}
	return 0;
}
