#include "ga.hh"
#include "chromosome.hh"
#include <tuple>
#include <iostream>
#include <set>
using namespace ga;

GeneticAlgorithm::GeneticAlgorithm(Evaluation::Type eval_type, Variation::Type var_type, int pop_size) {
  switch(eval_type) {
    case Evaluation::BANANA:
      this->evaluator = BANANA_FUNC;
      this->norm_min = BANANA_FUNC_MIN;
      this->norm_max = BANANA_FUNC_MAX;
      this->var_count = BANANA_FUNC_VAR_COUNT;
      break;
    case Evaluation::GOLDSTEIN_PRICE:
      this->evaluator = GOLDSTEIN_PRICE_FUNC;
      this->norm_min = GOLDSTEIN_PRICE_FUNC_MIN;
      this->norm_max = GOLDSTEIN_PRICE_FUNC_MAX;
      this->var_count = GOLDSTEIN_PRICE_VAR_COUNT;
  }

  this->var_type = var_type;
  this->pop_size = pop_size;
}


std::vector<double> GeneticAlgorithm::run() {
  int pop_split = this->pop_size / 2;
  std::set<std::pair<Chromosome*, double>, pair_compare> population;
  for(int i = 0; i < this->pop_size; i++) {
    Chromosome* temp = new Chromosome(this->var_count, this->norm_min, this->norm_max);
    population.insert(std::make_pair(temp, this->evaluator(*temp)));
  }
  int TEMP_COUNTER_PLZ_DELETE = 0;
  while(true && TEMP_COUNTER_PLZ_DELETE < 1000) {
    //Select the top half
    auto it1 = population.begin();
    std::advance(it1, pop_split);

    while (it1 != population.end()) {
      auto temp = it1++;
      delete (*temp).first;
      population.erase(temp);
    }

    //variation
    Chromosome* best = (*population.begin()).first;
    std::vector<Chromosome*> temp_vec;
    for(auto it2 = ++population.begin(); it2 != population.end(); ++it2) {
      switch(this->var_type) {
        case Variation::CROSSOVER:
          int index = best->get_rand_index();
          temp_vec.push_back(new Chromosome(best, (*it2).first, index));
          temp_vec.push_back(new Chromosome((*it2).first, best, index));
          break;
      }
    }

    for(int i = 0; i < temp_vec.size(); i++) {
      population.insert(std::make_pair(temp_vec[i], this->evaluator(*temp_vec[i])));
    }
    //update population
    auto it3 = population.begin();
    std::advance(it3, this->pop_size);
    while (it3 != population.end()) {
      auto temp = it3++;
      delete (*temp).first;
      population.erase(temp);
    }

    TEMP_COUNTER_PLZ_DELETE++;
  } 

  std::cout << "Finished, min val: " << (*population.begin()).second << std::endl;
  std::vector<double> retval = (*population.begin()).first->get_params();

  for(auto it = population.begin(); it != population.end(); ++it) {
    delete (*it).first;
  }

  return retval;
}



