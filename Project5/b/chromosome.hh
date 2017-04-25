/**
* chromosome.hh
*
* The header file for the declaration of the Chromosome object
* Author: Austin Doolittle
**/

#ifndef CHROMOSOME_HH
#define CHROMOSOME_HH
#include <vector>

#define INT_SIZE (sizeof(int) * 8)

namespace ga {
  class Chromosome {
  public:
    Chromosome(int var_count, double norm_min, double norm_max);
    Chromosome(Chromosome* c1, Chromosome* c2, int index);
    Chromosome(Chromosome* c, int mutate_prob);
    double operator[](int index);
    int size();
    int get_rand_index();
    std::vector<double> get_params();
  private:
    int var_count;
    double min;
    double max;
    std::vector<int> bitstring;
    double normalize(int val);
  };
}





#endif