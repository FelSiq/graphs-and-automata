FLAGS = -Wall -I ./ -DDEBUG -g
OUTPUT_FILE = rubik-solver

all: main.tag heap.tag rubik.tag
	gcc -o $(OUTPUT_FILE) main.o heap.o rubik.o $(FLAGS) && rm *.o
main.tag:
	gcc -c main.c $(FLAGS)
rubik.tag:
	gcc -c rubik.c $(FLAGS)
heap.tag:
	gcc -c heap.c $(FLAGS)
