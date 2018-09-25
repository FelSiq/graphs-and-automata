FLAGS = -Wall -I ./
OUTPUT_FILE = rubik-solver

all: main.tag rubik.tag
	gcc -o $(OUTPUT_FILE) main.o rubik.o $(FLAGS) && rm *.o
main.tag:
	gcc -c main.c $(FLAGS)
rubik.tag:
	gcc -c rubik.c $(FLAGS)
