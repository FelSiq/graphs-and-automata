#include <stdlib.h>
#include <stdio.h>
#include <rubik.h>
#include <string.h>

struct rubik_struct {
	color_type config[COLOR_NUM][ROW_NUM][COL_NUM],
		*p_c[COLOR_NUM][ROW_NUM + 2][COL_NUM + 2];
	unsigned char sol_size, *solution;
};

static void __build_pointer_matrix__(rubik *restrict r) {
	color_type *p_G_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{NULL, &r->config[C_W][0][0], &r->config[C_W][1][0], &r->config[C_W][2][0], NULL},
		{&r->config[C_O][0][2], &r->config[C_G][0][0], &r->config[C_G][0][1], &r->config[C_G][0][2], &r->config[C_R][0][0]},
		{&r->config[C_O][1][2], &r->config[C_G][1][0], &r->config[C_G][1][1], &r->config[C_G][1][2], &r->config[C_R][1][0]},
		{&r->config[C_O][2][2], &r->config[C_G][2][0], &r->config[C_G][2][1], &r->config[C_G][2][2], &r->config[C_R][2][0]},
		{NULL, &r->config[C_Y][2][0], &r->config[C_Y][1][0], &r->config[C_Y][0][0], NULL},
	};

	color_type *p_O_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{NULL, &r->config[C_W][0][2], &r->config[C_W][0][1], &r->config[C_W][0][0], NULL},
		{&r->config[C_B][0][2], &r->config[C_O][0][0], &r->config[C_O][0][1], &r->config[C_O][0][2], &r->config[C_G][0][0]},
		{&r->config[C_B][1][2], &r->config[C_O][1][0], &r->config[C_O][1][1], &r->config[C_O][1][2], &r->config[C_G][1][0]},
		{&r->config[C_B][2][2], &r->config[C_O][2][0], &r->config[C_O][2][1], &r->config[C_O][2][2], &r->config[C_G][2][0]},
		{NULL, &r->config[C_Y][2][0], &r->config[C_Y][2][1], &r->config[C_Y][2][2], NULL},
	};

	color_type *p_B_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{NULL, &r->config[C_W][2][2], &r->config[C_W][1][2], &r->config[C_W][0][2], NULL},
		{&r->config[C_R][0][2], &r->config[C_B][0][0], &r->config[C_B][0][1], &r->config[C_B][0][2], &r->config[C_O][0][0]},
		{&r->config[C_R][1][2], &r->config[C_B][1][0], &r->config[C_B][1][1], &r->config[C_B][1][2], &r->config[C_O][1][0]},
		{&r->config[C_R][2][2], &r->config[C_B][2][0], &r->config[C_B][2][1], &r->config[C_B][2][2], &r->config[C_O][2][0]},
		{NULL, &r->config[C_Y][0][2], &r->config[C_Y][1][2], &r->config[C_Y][2][2], NULL},
	};

	color_type *p_Y_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{NULL, &r->config[C_R][2][0], &r->config[C_R][2][1], &r->config[C_R][2][2], NULL},
		{&r->config[C_G][2][2], &r->config[C_Y][0][0], &r->config[C_Y][0][1], &r->config[C_Y][0][2], &r->config[C_B][2][0]},
		{&r->config[C_G][2][1], &r->config[C_Y][1][0], &r->config[C_Y][1][1], &r->config[C_Y][1][2], &r->config[C_B][2][1]},
		{&r->config[C_G][2][0], &r->config[C_Y][2][0], &r->config[C_Y][2][1], &r->config[C_Y][2][2], &r->config[C_B][2][2]},
		{NULL, &r->config[C_O][2][2], &r->config[C_O][2][1], &r->config[C_O][2][0], NULL},
	};

	color_type *p_R_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{NULL, &r->config[C_W][2][0], &r->config[C_W][2][1], &r->config[C_W][2][2], NULL},
		{&r->config[C_G][0][2], &r->config[C_R][0][0], &r->config[C_R][0][1], &r->config[C_R][0][2], &r->config[C_B][0][0]},
		{&r->config[C_G][1][2], &r->config[C_R][1][0], &r->config[C_R][1][1], &r->config[C_R][1][2], &r->config[C_B][1][0]},
		{&r->config[C_G][2][2], &r->config[C_R][2][0], &r->config[C_R][2][1], &r->config[C_R][2][2], &r->config[C_B][2][0]},
		{NULL, &r->config[C_Y][0][0], &r->config[C_Y][0][1], &r->config[C_Y][0][2], NULL},
	};

	color_type *p_W_mat[ROW_NUM + 2][COL_NUM + 2] = {
		{NULL, &r->config[C_O][0][2], &r->config[C_O][0][1], &r->config[C_O][0][0], NULL},
		{&r->config[C_G][0][0], &r->config[C_W][0][0], &r->config[C_W][0][1], &r->config[C_W][0][2], &r->config[C_B][0][2]},
		{&r->config[C_G][0][1], &r->config[C_W][1][0], &r->config[C_W][1][1], &r->config[C_W][1][2], &r->config[C_B][0][1]},
		{&r->config[C_G][0][2], &r->config[C_W][2][0], &r->config[C_W][2][1], &r->config[C_W][2][2], &r->config[C_B][0][0]},
		{NULL, &r->config[C_R][0][0], &r->config[C_R][0][1], &r->config[C_R][0][2], NULL},
	};

	memcpy(r->p_c[C_W], p_W_mat, sizeof(p_W_mat));
	memcpy(r->p_c[C_Y], p_Y_mat, sizeof(p_Y_mat));
	memcpy(r->p_c[C_G], p_G_mat, sizeof(p_G_mat));
	memcpy(r->p_c[C_R], p_R_mat, sizeof(p_R_mat));
	memcpy(r->p_c[C_B], p_B_mat, sizeof(p_B_mat));
	memcpy(r->p_c[C_O], p_O_mat, sizeof(p_O_mat));
}

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

		// Build up pointer matrices
		__build_pointer_matrix__(r);
	} 

	return r;
}

int rubik_print(const rubik *const restrict r) {
	if (r != NULL) {
		register unsigned char i, row, col, color;
		const char offset[] = "      ";
		for (i = 0; i < sizeof(PRINT_COLOR_SEQ)/sizeof(char); i++) {
			color = (int) PRINT_COLOR_SEQ[i] - (int) '0';
			printf("%s", (color == C_W || color == C_Y) ? offset : ""); 
			for (col = 0; col < COL_NUM; col++) {
				printf("%c ", r->config[color][row][col]);
			}
			printf("%c", PRINT_BREAKLINE[i]);
			row = (row + PRINT_BREAKLINE[i] == '\n') % ROW_NUM;
		}
		printf("\n");
		return 1;
	}
	return 0;
}

int rubik_solve(const rubik *restrict r) {
	if (r == NULL)
		return 0;
	return 1;
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
