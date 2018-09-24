#ifndef __RUBIK_SOLVING__
#define __RUBIK_SOLVING__

/* TYPEDEF & DEFINE SECTION */

#define COLOR_NUM 6
char const restrict COLORS[] = "WYGRBO";

#define COL_NUM 3
#define ROW_NUM 3

typedef unsigned char color_type;

enum {
	PROGNAME,
	FILEPATH,
	SEPARATOR,
	ARGSNUM
};

typedef struct {
	color_type config[COLOR_NUM][COL_NUM][ROW_NUM],
		*p_r[COL_NUM + 2][ROW_NUM + 2],
		*p_w[COL_NUM + 2][ROW_NUM + 2],
		*p_b[COL_NUM + 2][ROW_NUM + 2],
		*p_g[COL_NUM + 2][ROW_NUM + 2],
		*p_o[COL_NUM + 2][ROW_NUM + 2],
		*p_y[COL_NUM + 2][ROW_NUM + 2];
} rubik;

/* FUNCTION DECLARATIONS */
rubik *rubik_create(char *const restrict filepath, char *const restrict sep);
int rubik_print(const rubik *restrict r);
int rubik_solve(const rubik *restrict r);
int rubik_solution(const rubik *restrict r);
int rubik_destroy(const rubik **restrict r);

#endif
