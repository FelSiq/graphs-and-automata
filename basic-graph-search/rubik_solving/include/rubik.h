#ifndef __RUBIK_SOLVING__
#define __RUBIK_SOLVING__

/* TYPEDEF & DEFINE SECTION */

// Enables use of IDA*. If false, use A*, which
// consumes way too much memory.
#define ENABLE_IDA_STAR 0
#define IDA_DEGREES_OF_FREEDOM 2

#ifndef MIN
	#define MIN(A, B) (((A) < (B)) ? (A) : (B))
#endif

#ifndef INFINITY
	#define INFINITY 255
#endif

// Number of sides of the cube
// Note that the code will mainly focus on solving a
// 3x3x3 Rubik's cube
#define COLOR_NUM 6
#define COL_NUM 3
#define ROW_NUM 3

#define COLOR_SEQ "WYGBRO"
#define C_W 		0b00000000
#define C_Y 		0b00000001
#define C_G 		0b00000010
#define C_B 		0b00000011
#define C_R 		0b00000100
#define C_O 		0b00000101
#define DIR_CLKWISE 	0b00000000
#define DIR_C_CLKWISE 	0b01000000
#define MASK_COL	0b00000111
#define MASK_DIR 	0b01000000
#define PRINT_COLOR_SEQ "000243524352435111"
#define PRINT_BREAKLINE "\n\n\n\0\0\0\n\0\0\0\n\0\0\0\n\n\n\n"

#define OPPOSITE_COLORS(C1, C2) (((C1) ^ (C2)) == 1) 

typedef unsigned char color_type;

struct rubik_struct {
	color_type config[COLOR_NUM][ROW_NUM][COL_NUM],
		INITIAL_CONFIG[COLOR_NUM][ROW_NUM][COL_NUM],
		*p_c[COLOR_NUM][ROW_NUM + 2][COL_NUM + 2],
		aux_p_c[ROW_NUM + 2][COL_NUM + 2];
	unsigned char sol_size, *solution, nil_pos;
};

typedef struct rubik_struct rubik;

enum {
	ARGV_PROGNAME,
	ARGV_FILEPATH,
	ARGV_SEPARATOR,
	ARGV_ARGSNUM
};

/* FUNCTION DECLARATIONS */
rubik *rubik_create(char *const restrict filepath);
int rubik_print(const rubik *const restrict r);
int rubik_solve(rubik *restrict r);
int rubik_solution(const rubik *const restrict r);
int rubik_destroy(rubik **restrict r);
int rubik_reinit(rubik *restrict r);
int rubik_rotate(rubik *restrict r, 
	unsigned char const color, 
	unsigned char const clockwise);

#endif
