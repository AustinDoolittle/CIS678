#include "chromosome.hh"
#include <vector>
#include <stdexcept>
#include <string>
#include <random>
#include <iostream>
#include <functional>

using namespace ga;


Chromosome::Chromosome(int var_count, double norm_min, double norm_max) {
  this->var_count = var_count;
  this->min = norm_min;
  this->max = norm_max;

  for(int i = 0; i < var_count; i++) {
    int random_val = std::rand();
    for(int i = 0; i < VAR_SIZE; i++) {
      this->bitstring.push_back((bool)(random_val & 1));
      random_val >>= 1;
    }
  }
}

Chromosome::Chromosome(Chromosome* c1, Chromosome* c2, int index) {
  this->var_count = c1->var_count;
  this->min = c1->min;
  this->max = c1->max;
  for(int i = 0; i < index; i++) {
    this->bitstring.push_back(c1->bitstring[i]);
  }
  for(int j = index; j < c1->bitstring.size(); j++) {
    this->bitstring.push_back(c2->bitstring[j]);
  }
}

double Chromosome::operator[](int index) {
  if (index < 0 || index >= this->var_count) {
    throw std::out_of_range("Got index " + std::to_string(index) + ", bounds [0-" + std::to_string(this->var_count - 1) + "]");
  }

  auto start = this->bitstring.begin() + (index * VAR_SIZE) - 1;
  auto end = start + VAR_SIZE;

  int int_convert = 0;
  while (start != end) {
    int_convert <<= 1;
    int_convert += (int)*end;
    end--;
  }
  return this->normalize(int_convert);
}

int Chromosome::size() {
  return this->var_count;
}

double Chromosome::normalize(int val) {
  return ((this->max - this->min) * ((double)val / (double)RAND_MAX + 0.0)) + this->min;
}

int Chromosome::get_rand_index() {
  return std::rand() % this->bitstring.size();
}

std::vector<double> Chromosome::get_params() {
  std::vector<double> retval;
  for(int i = 0; i < this->size(); i++) {
    retval.push_back(this->operator[](i));
  }
  return retval;
}
