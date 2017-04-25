/**
* chromosome.cc
*
* Contains the implementation of the Chromosome object functions
* Author: Austin Doolittle
**/

#include "chromosome.hh"
#include <vector>
#include <stdexcept>
#include <stdlib.h>
#include <string>
#include <functional>

using namespace ga;

//Declare the default chromosome constructor
Chromosome::Chromosome(int var_count, double norm_min, double norm_max) {
  this->var_count = var_count;
  this->min = norm_min;
  this->max = norm_max;

  //for each variable, add its bits to the bitstring
  for(int i = 0; i < var_count; i++) {
    int random_val = rand();
    for(int j = 0; j < VAR_SIZE; j++) {
      this->bitstring.push_back((bool)(random_val & 1));
      random_val >>= 1;
    }
  }
}

//Creates a new chromosome by splicing two prexisting chromosomes
Chromosome::Chromosome(Chromosome* c1, Chromosome* c2, int index) {
  this->var_count = c1->var_count;
  this->min = c1->min;
  this->max = c1->max;

  //iterate until the split index and splice
  for(int i = 0; i < index; i++) {
    this->bitstring.push_back(c1->bitstring[i]);
  }
  for(int j = index; j < c1->bitstring.size(); j++) {
    this->bitstring.push_back(c2->bitstring[j]);
  }
}

//Constructor for creating a mutation of another chromosome
Chromosome::Chromosome(Chromosome* c, int mutate_prob) {
  this->var_count = c->var_count;
  this->min = c->min;
  this->max = c->max;
  for(int i = 0; i < c->bitstring.size(); i++) {
    //flip bit
    //prevent the sign bit from flipping (we don't want negative numbers, screws up our normalization)
    if((i % VAR_SIZE != (VAR_SIZE - 1)) && rand() % mutate_prob == 0) {
      this->bitstring.push_back(!c->bitstring[i]);
    }
    else {
      this->bitstring.push_back(c->bitstring[i]);
    }
  }
}

//Accessor operatior
double Chromosome::operator[](int index) {
  //check for out of bounds
  if (index < 0 || index >= this->var_count) {
    throw std::out_of_range("Got index " + std::to_string(index) + ", bounds [0-" + std::to_string(this->var_count - 1) + "]");
  }

  //get the start and end of this value
  auto start = this->bitstring.begin() + (index * VAR_SIZE) - 1;
  auto end = start + VAR_SIZE;

  //iterate and create the object
  int int_convert = 0;
  while (start != end) {
    int_convert <<= 1;
    int_convert += (int)*end;
    end--;
  }
  return this->normalize(int_convert);
}

//Returns the number of variables
int Chromosome::size() {
  return this->var_count;
}

//normalizes the value between the limits provided
double Chromosome::normalize(int val) {
  return (this->max - this->min)*(((double)val)/((double)RAND_MAX)) + this->min;
}

//returns a random value in the bounds of the index
int Chromosome::get_rand_index() {
  return rand() % this->bitstring.size();
}

//returns a vector of the parameters stored in the chromosome
std::vector<double> Chromosome::get_params() {
  std::vector<double> retval;
  for(int i = 0; i < this->size(); i++) {
    retval.push_back(this->operator[](i));
  }
  return retval;
}
