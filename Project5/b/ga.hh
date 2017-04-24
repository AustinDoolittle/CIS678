#ifndef GA_HH
#define GA_HH

#include <vector>
#include "chromosome.hh"
#include <functional>
#include <tuple>

#define BANANA_FUNC_MIN -2.0
#define BANANA_FUNC_MAX 3.0
#define BANANA_FUNC_VAR_COUNT 2
#define BANANA_FUNC_TERM 5.0e-16
#define GOLDSTEIN_PRICE_FUNC_MIN -2.0
#define GOLDSTEIN_PRICE_FUNC_MAX 2.0
#define GOLDSTEIN_PRICE_VAR_COUNT 2
#define GOLDSTEIN_PRICE_TERM 3
#define GA_FUNC_MIN 100
#define GA_FUNC_MAX 2500
#define GA_VAR_COUNT 3
#define GA_MAX_ITERS 100000
#define GA_TERM 0

namespace Evaluation {
  enum Type {
    BANANA,
    GOLDSTEIN_PRICE,
    GA_BANANA,
    GA_GOLDSTEIN_PRICE
  };
}

namespace ga {

  struct pair_compare {
    bool operator() (const std::pair<Chromosome*, double>& lhs, const std::pair<Chromosome*, double>& rhs) const{
        return lhs.second <= rhs.second;
    }
  };

  class GeneticAlgorithm {
  public:
   GeneticAlgorithm(Evaluation::Type eval_type, int pop_size);
   std::vector<double> run(int max_iterations, bool verbose);
   std::vector<double> run(int max_iterations, bool verbose, int mutate_count);
  private:
    std::function<double (Chromosome*)> evaluator;
    int pop_size;
    double norm_min;
    double norm_max;
    int var_count;
    double term_val;
    Chromosome* crossover(Chromosome* c1, Chromosome* c2);
    double static goldstein_price(Chromosome* c);
    double static banana(Chromosome* c);
    double static ga_banana(Chromosome* c);
    double static ga_goldstein_price(Chromosome* c);
  };
}


#endif