#include "ga.hh"
#include "chromosome.hh"
#include <tuple>
#include <iostream>
#include <set>
#include <time.h>
#include <random>
using namespace ga;

GeneticAlgorithm::GeneticAlgorithm(Evaluation::Type eval_type, int pop_size) {
  switch(eval_type) {
    case Evaluation::BANANA:
      this->evaluator = this->banana;
      this->norm_min = BANANA_FUNC_MIN;
      this->norm_max = BANANA_FUNC_MAX;
      this->var_count = BANANA_FUNC_VAR_COUNT;
      this->term_val = BANANA_FUNC_TERM;
      break;
    case Evaluation::GOLDSTEIN_PRICE:
      this->evaluator = this->goldstein_price;
      this->norm_min = GOLDSTEIN_PRICE_FUNC_MIN;
      this->norm_max = GOLDSTEIN_PRICE_FUNC_MAX;
      this->var_count = GOLDSTEIN_PRICE_VAR_COUNT;
      this->term_val = GOLDSTEIN_PRICE_TERM;
      break;
    case Evaluation::GA_GOLDSTEIN_PRICE:
      this->evaluator = this->ga_goldstein_price;
      this->norm_min = GA_FUNC_MIN;
      this->norm_max = GA_FUNC_MAX;
      this->var_count = GA_VAR_COUNT;
      this->term_val = GA_TERM;
      break;
    case Evaluation::GA_BANANA:
      this->evaluator = this->ga_banana;
      this->norm_min = GA_FUNC_MIN;
      this->norm_max = GA_FUNC_MAX;
      this->var_count = GA_VAR_COUNT;
      this->term_val = GA_TERM;
      break;
  }

  this->pop_size = pop_size;
}

std::vector<double> GeneticAlgorithm::run(int max_iterations, bool verbose) {
  return GeneticAlgorithm::run(max_iterations, verbose, this->pop_size);
}

std::vector<double> GeneticAlgorithm::run(int max_iterations, bool verbose, int mutate_count) {
  /**
  * SELECTION 
  *
  * Determined automatically on item insertion into the set by sorting on
  * the calculated value in the function
  **/
  std::set<std::pair<Chromosome*, double>, pair_compare> population;
  for(int i = 0; i < this->pop_size; i++) {
    Chromosome* temp = new Chromosome(this->var_count, this->norm_min, this->norm_max);
    population.insert(std::make_pair(temp, this->evaluator(temp)));
  }

  int counter = 0;
  while(counter < max_iterations) {
    counter++;

    /**
    * VARIATION
    *
    * Crossover - perform with the best chromosome and all other chromosomes
    * Mutation - perform current population size / 2 mutations on the best item
    **/

    //Crossover
    Chromosome* best= (*population.begin()).first;
    std::vector<Chromosome*> temp_vec;
    for(auto it2 = ++population.begin(); it2 != population.end(); ++it2) {
      int index = best->get_rand_index();
      temp_vec.push_back(new Chromosome(best, (*it2).first, index));
      temp_vec.push_back(new Chromosome((*it2).first, best, index));
    }

    for(int i = 0; i < temp_vec.size(); i++) {
      population.insert(std::make_pair(temp_vec[i], this->evaluator(temp_vec[i])));
    }

    //Mutation
    int mutate_count = population.size();
    for(int j = 0; j < mutate_count; j++) {
      Chromosome* temp_c = new Chromosome((*population.begin()).first);
      population.insert(std::make_pair(temp_c,this->evaluator(temp_c)));
    }

    if (verbose) {
      std::cout << "\tIteration " << counter << "/" << max_iterations << ", min: " << (*population.begin()).second << std::endl;
    }

    /**
    * UPDATE
    *
    * Trim to the population size
    */
    auto it3 = population.begin();
    std::advance(it3, this->pop_size);
    while (it3 != population.end()) {
      auto temp = it3++;
      delete (*temp).first;
      population.erase(temp);
    }

    /**
    * TERMINATION
    *
    * Check if we have the correct output
    **/
    if ((*population.begin()).second <= this->term_val) {
      break;
    }
  } 

  if(verbose) {
    std::cout << "Finished in " << counter << " iterations, min val: " << (*population.begin()).second << std::endl;
  }

  std::vector<double> retval = (*population.begin()).first->get_params();

  for(auto it = population.begin(); it != population.end(); ++it) {
    delete (*it).first;
  }

  return retval;
}

double GeneticAlgorithm::goldstein_price(Chromosome* c) {
  return (std::pow((*c)[0] + (*c)[1] + 1, 2) * (19 - 14 * (*c)[0] + 3 * std::pow((*c)[0],2) - 14 * (*c)[1] + 6 * (*c)[0] * (*c)[1] + 3 * std::pow((*c)[1],2)) + 1) * 
                                                      ((std::pow(2 * (*c)[0] - 3 * (*c)[1], 2) * 
                                                      (18 - 32 * (*c)[0] + 12 * std::pow((*c)[0], 2) + 48 * (*c)[1] - 36 * (*c)[0] * (*c)[1] + 27 * std::pow((*c)[1],2))) + 30);
}

double GeneticAlgorithm::banana(Chromosome* c) {
  return std::pow(1 - (*c)[0], 2) + 100 * std::pow(((*c)[1] - std::pow((*c)[0], 2)), 2);
}

double GeneticAlgorithm::ga_banana(Chromosome* c) {
  std::srand((*c)[0]);
  GeneticAlgorithm ga(Evaluation::BANANA, (*c)[1]);
  std::clock_t ts = std::clock();
  ga.run(GA_MAX_ITERS, false, (*c)[2]);
  std::clock_t te = std::clock();
  return ((float)te - (float)ts) / CLOCKS_PER_SEC;
}

double GeneticAlgorithm::ga_goldstein_price(Chromosome* c) {
  std::srand((*c)[0]);
  GeneticAlgorithm ga(Evaluation::GOLDSTEIN_PRICE, (*c)[1]);
  std::clock_t ts = std::clock();
  ga.run(GA_MAX_ITERS, false, (*c)[2]);
  std::clock_t te = std::clock();
  return ((float)te - (float)ts) / CLOCKS_PER_SEC;
}

