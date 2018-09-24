#include <stdio.h>
#include <rubik.h>

int main(int argc, char *const argv[]) {
	if (argc < ARGSNUM) {
		printf("usage: %s <filepath>"
			" [separator - default to \",\"]\n", argv[PROGNAME]);
		return 1;
	}
	
	char sep = ",";
	if (argc == 2)
		sep = argv[SEPARATOR];

	if ((const rubik *r = rubik_create(argv[FILEPATH], sep)) == NULL)
		printf("Error: something went wrong"
			" when loading cube configuration.\n");
		return 2;
	}

	printf("Loaded configuration:\n");
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
