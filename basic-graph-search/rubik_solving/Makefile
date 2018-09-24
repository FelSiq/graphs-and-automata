FLAGS = -Wall -I ./
OUTPUT_FILE = rubik

all: main rubik
	gcc -o $(OUTPUT_FILE) main.o rubik.o $(FLAGS) && rm *.o
main:
	gcc -c main.c $(FLAGS)
rubik:
	gcc -c rubik.c $(FLAGS)
