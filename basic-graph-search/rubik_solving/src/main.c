#include <stdio.h>
#include <rubik.h>

int main(int argc, char *const argv[]) {
	if (argc < ARGV_ARGSNUM - 1) {
		printf("usage: %s <filepath>\n", argv[ARGV_PROGNAME]);
		return 1;
	}

	rubik *r = rubik_create(argv[ARGV_FILEPATH]);

	if (r == NULL) {
		printf("Error: something went wrong"
			" when loading cube configuration.\n");
		return 2;
	}

	#if INIT_CONFIG
		rubik_rotate(r, C_W, DIR_CLKWISE);
		rubik_rotate(r, C_R, DIR_C_CLKWISE);
		rubik_rotate(r, C_B, DIR_CLKWISE);
		rubik_rotate(r, C_Y, DIR_CLKWISE);
		rubik_rotate(r, C_Y, DIR_CLKWISE);
		rubik_rotate(r, C_O, DIR_C_CLKWISE);
		rubik_rotate(r, C_R, DIR_CLKWISE);
		rubik_rotate(r, C_G, DIR_C_CLKWISE);
		rubik_rotate(r, C_O, DIR_C_CLKWISE);
		rubik_rotate(r, C_O, DIR_C_CLKWISE);
		rubik_rotate(r, C_W, DIR_CLKWISE);
		rubik_rotate(r, C_Y, DIR_C_CLKWISE);
		rubik_rotate(r, C_B, DIR_C_CLKWISE);
		rubik_rotate(r, C_G, DIR_C_CLKWISE);
		rubik_rotate(r, C_G, DIR_C_CLKWISE);
		rubik_rotate(r, C_Y, DIR_CLKWISE);
		rubik_reinit(r);
	#endif

	printf("Start configuration:\n");
	rubik_print(r);

	printf("Solving...\n");
	rubik_solve(r);

	printf("Result:\n");
	rubik_print(r);

	printf("Step by step solution:\n");
	rubik_solution(r);

	if (rubik_destroy(&r) == 0)
		printf("Warning: possible memory leaks.\n");

	return 0;
}
