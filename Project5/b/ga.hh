#ifndef GA_HH
#define GA_HH

#include <vector>
#include "chromosome.hh"
#include <functional>
#include <tuple>

#define BANANA_FUNC [] (ga::Chromosome c) {return std::pow(1 - c[0], 2) + 100 * std::pow((c[1] - std::pow(c[0], 2)), 2);}
#define BANANA_FUNC_MIN -2.0
#define BANANA_FUNC_MAX 3.0
#define BANANA_FUNC_VAR_COUNT 2
#define GOLDSTEIN_PRICE_FUNC [](ga::Chromosome c) {return (std::pow(c[0] + c[1] + 1, 2) * (19 - 14 * c[0] + 3 * std::pow(c[0],2) - 14 * c[1] + 6 * c[0] * c[1] + 3 * std::pow(c[1],2)) + 1) * \
                                                      ((std::pow(2 * c[0] - 3 * c[1], 2) * \
                                                      (18 - 32 * c[0] + 12 * std::pow(c[0], 2) + 48 * c[1] - 36 * c[0] * c[1] + 27 * std::pow(c[1],2))) + 30);}
#define GOLDSTEIN_PRICE_FUNC_MIN -2.0
#define GOLDSTEIN_PRICE_FUNC_MAX 2.0
#define GOLDSTEIN_PRICE_VAR_COUNT 2

namespace Variation {
  enum Type {
    CROSSOVER,
    MUTATION
  };
}

namespace Evaluation {
  enum Type {
    BANANA,
    GOLDSTEIN_PRICE
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
   GeneticAlgorithm(Evaluation::Type eval_type, Variation::Type var_type, int pop_size);
   std::vector<double> run();
  private:
    std::function<double (Chromosome)> evaluator;
    Variation::Type var_type;
    int pop_size;
    double norm_min;
    double norm_max;
    int var_count;
    //Chromosome* mutation(Chromosome* c);
    Chromosome* crossover(Chromosome* c1, Chromosome* c2);
  };
}


#endif