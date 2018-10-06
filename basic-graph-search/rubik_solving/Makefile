SOURCE_PATH = ./src
INCLUDE_PATH = ./include
MAINFLAGS = -D INIT_CONFIG
FLAGS = -Wall -I $(INCLUDE_PATH) -O3 -Wextra -D ENABLE_IDA_STAR
OUTPUT_FILE = rubik-solver

all: main.tag heap.tag stack.tag rubik.tag
	gcc -o $(OUTPUT_FILE) main.o heap.o rubik.o stack.o $(FLAGS) && rm *.o
main.tag:
	gcc -c $(SOURCE_PATH)/main.c $(FLAGS) $(MAINFLAGS)
rubik.tag:
	gcc -c $(SOURCE_PATH)/rubik.c $(FLAGS)
heap.tag:
	gcc -c $(SOURCE_PATH)/heap.c $(FLAGS)
stack.tag:
	gcc -c $(SOURCE_PATH)/stack.c $(FLAGS)
