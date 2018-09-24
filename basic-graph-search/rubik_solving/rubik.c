#include <stdlib.h>
#include <stdio.h>
#include <rubik.h>
#include <string.h>

struct rubik_struct {
	color_type config[COLOR_NUM][COL_NUM][ROW_NUM],
		*p_r[COL_NUM + 2][ROW_NUM + 2],
		*p_w[COL_NUM + 2][ROW_NUM + 2],
		*p_b[COL_NUM + 2][ROW_NUM + 2],
		*p_g[COL_NUM + 2][ROW_NUM + 2],
		*p_o[COL_NUM + 2][ROW_NUM + 2],
		*p_y[COL_NUM + 2][ROW_NUM + 2];

	unsigned char sol_size, *solution;
};


rubik *rubik_create(char *const restrict filepath, char const sep[]) {
	rubik *r = NULL;

	FILE *restrict input_f = fopen(filepath, "r");
	
	if (input_f != NULL) {

		register unsigned char color, row, col;
		const unsigned long sep_size = strlen(sep);
		char *read_pattern = malloc(sizeof(char) * 
			(1 + (2*COLOR_NUM + sep_size) * COL_NUM));

		for (col = 0; col < COL_NUM; col++) {
			read_pattern = strcat(read_pattern, "%c");
			if (sep_size > 0 && col != COL_NUM - 1)
				read_pattern = strcat(read_pattern, sep);
		}
		printf("test: %s\n", read_pattern);

		r = malloc(sizeof(rubik));

		if (r != NULL) {
			r->sol_size = 0;
			r->solution = NULL;

			for (color = 0; color < COLOR_NUM; color++)
				for (row = 0; row < ROW_NUM; row++)
					fscanf(input_f, read_pattern, r->config[color][row]);
		}

		free(read_pattern);
		fclose(input_f);
	} 

	return r;
}

int rubik_print(const rubik *const restrict r) {
	if (r != NULL) {
		//register unsigned char color, row, col;
	}
	return 0;
}

int rubik_solve(const rubik *restrict r) {
	return 1;
}

int rubik_solution(const rubik *const restrict r) {
	if (r != NULL) {
		for (register unsigned char i = 0; i < r->sol_size; i += 2)
			printf("%hhu\t: %hhu %s", i, r->solution[i], 
				r->solution[i + 1] == '1' ? "->" : "<-");

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
