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
#include <iostream>

using namespace ga;

//Declare the default chromosome constructor
Chromosome::Chromosome(int var_count, double norm_min, double norm_max) {
  this->var_count = var_count;
  this->min = norm_min;
  this->max = norm_max;

  //for each variable, add its bits to the bitstring
  for(int i = 0; i < var_count; i++) {
    int random_val = rand();
    this->bitstring.push_back(random_val);
  }
}

//Creates a new chromosome by splicing two prexisting chromosomes
Chromosome::Chromosome(Chromosome* c1, Chromosome* c2, int index) {
  this->var_count = c1->var_count;
  this->min = c1->min;
  this->max = c1->max;

  //iterate until the split index and splice
  int sub_index = index % INT_SIZE;
  int sup_index = index - sub_index;
  for(int i = 0; i < c1->bitstring.size(); i++) {
    if (i == sup_index) {
      //trim bits off front of bitstring
      int temp_2 = ((c2->bitstring[i] << (sub_index)) >> (sub_index));

      //trim bits off end of bistring
      int temp_1 = ((c1->bitstring[i] >> ((INT_SIZE - sub_index) + 1)) << ((INT_SIZE - sub_index) + 1));

      //combine
      this->bitstring.push_back(temp_1 | temp_2);
    }
    else if (i < sup_index) {
      this->bitstring.push_back(c1->bitstring[i]);
    }
    else {
      this->bitstring.push_back(c2->bitstring[i]);
    }
  }
}

//Constructor for creating a mutation of another chromosome
Chromosome::Chromosome(Chromosome* c, int mutate_prob) {
  this->var_count = c->var_count;
  this->min = c->min;
  this->max = c->max;
  for(int i = 0; i < c->bitstring.size(); i++) {
    //create mask and xor with other bitstring values
    int mask = 0;
    for(int j = 0; j < INT_SIZE; j++) {
      mask <<= 1;
      if(j != 0 && rand() % mutate_prob == 0) {
        mask |= 1;
      }
    }
    this->bitstring.push_back(mask ^ c->bitstring[i]);
  }
}

//Accessor operatior
double Chromosome::operator[](int index) {
  //check for out of bounds
  if (index < 0 || index >= this->var_count) {
    throw std::out_of_range("Got index " + std::to_string(index) + ", bounds [0-" + std::to_string(this->var_count - 1) + "]");
  }
  return this->normalize(this->bitstring[index]);
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
  return rand() % (this->bitstring.size() * INT_SIZE);
}

//returns a vector of the parameters stored in the chromosome
std::vector<double> Chromosome::get_params() {
  std::vector<double> retval;
  for(int i = 0; i < this->size(); i++) {
    retval.push_back(this->operator[](i));
  }
  return retval;
}
