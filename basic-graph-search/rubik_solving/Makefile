SOURCE_PATH = ./src
INCLUDE_PATH = ./include
FLAGS = -Wall -I $(INCLUDE_PATH) -D INIT_CONFIG -O3
OUTPUT_FILE = rubik-solver

all: main.tag heap.tag rubik.tag
	gcc -o $(OUTPUT_FILE) main.o heap.o rubik.o $(FLAGS) && rm *.o
main.tag:
	gcc -c $(SOURCE_PATH)/main.c $(FLAGS)
rubik.tag:
	gcc -c $(SOURCE_PATH)/rubik.c $(FLAGS)
heap.tag:
	gcc -c $(SOURCE_PATH)/heap.c $(FLAGS)
