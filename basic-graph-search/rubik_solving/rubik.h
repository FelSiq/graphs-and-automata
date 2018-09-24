#ifndef __RUBIK_SOLVING__
#define __RUBIK_SOLVING__

/* TYPEDEF & DEFINE SECTION */

// Number of sides of the cube
// Note that the code will mainly focus on solving a
// 3x3x3 Rubik's cube
#define COLOR_NUM 6
#define COL_NUM 3
#define ROW_NUM 3
enum {
	C_W,
	C_Y,
	C_G,
	C_R,
	C_B,
	C_O
};

typedef unsigned char color_type;
typedef struct rubik_struct rubik;

enum {
	ARGV_PROGNAME,
	ARGV_FILEPATH,
	ARGV_SEPARATOR,
	ARGV_ARGSNUM
};

/* FUNCTION DECLARATIONS */
rubik *rubik_create(char *const restrict filepath, char const sep[]);
int rubik_print(const rubik *const restrict r);
int rubik_solve(const rubik *restrict r);
int rubik_solution(const rubik *const restrict r);
int rubik_destroy(rubik **restrict r);

#endif
