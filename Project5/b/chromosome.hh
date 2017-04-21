#ifndef CHROMOSOME_HH
#define CHROMOSOME_HH
#include <vector>
#include <cmath>

#define VAR_SIZE 8 * sizeof(int)



namespace ga {
  class Chromosome {
  public:
    Chromosome(int var_count, double norm_min, double norm_max);
    Chromosome(Chromosome* c1, Chromosome* c2, int index);
    double operator[](int index);
    int size();
    int get_rand_index();
    std::vector<double> get_params();
  private:
    int var_count;
    double min;
    double max;
    std::vector<bool> bitstring;
    double normalize(int val);
  };
}





#endif