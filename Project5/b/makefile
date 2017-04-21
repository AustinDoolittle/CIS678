FLAGS=-std=c++11 -Wall
CXX=g++
OUT=ga.out
LIBS=-lboost_program_options

SRC=$(wildcard *.cc)
OBJ=$(SRC:%.cc=%.o)

all: $(OBJ)
	$(CXX) $(FLAGS) -o $(OUT) $^ $(LIBS)

%.o: %.cc
	$(CXX) $(FLAGS) $< -c -o $@

clean:
	rm -f *.o
	rm $(OUT)
