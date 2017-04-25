/**
* ga.cc
*
* Contains the implementations for the Genetic Algorithm class
* Author: Austin Doolittle
**/

#include "ga.hh"
#include "chromosome.hh"
#include <tuple>
#include <iostream>
#include <set>
#include <time.h>
#include <cmath>
#include <stdlib.h>

using namespace ga;

// Constructor for the Genetic Algorithm object
// eval_type is the type of function to perform the Genetic Algorithm on
// pop_size is the size of the population
GeneticAlgorithm::GeneticAlgorithm(Evaluation::Type eval_type, int pop_size) {

  //Setup the GA object based on the evaluation type
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

  //set the pop size
  this->pop_size = pop_size;
}

//The method for running the genetic algorithm on the given evaluation function
//max_iterations is the maximum iterations over the population
//verbose is the verbosity level
//mutate_prop is the probability of mutation (1/mutate_prop = probablity of mutation)
std::vector<double> GeneticAlgorithm::run(int max_iterations, int verbose, int mutate_prob, int mutate_count) {
  /**
  * SELECTION 
  *
  * Determined automatically on item insertion into the set by sorting on
  * the calculated value in the function
  **/

  if(verbose >= VERBOSE_LOW) {
    std::cout << "\tCreating initial population..." << std::endl;
  }

  std::set<std::pair<Chromosome*, double>, pair_compare> population;
  for(int i = 0; i < this->pop_size; i++) {

    if(verbose >= VERBOSE_HIGH) {
      std::cout << "\t\t\tInitial population " << (i + 1) << std::endl;
    }

    //Allocate Chromosome pointer
    Chromosome* temp = new Chromosome(this->var_count, this->norm_min, this->norm_max);
    population.insert(std::make_pair(temp, this->evaluator(temp)));
  }

  if(verbose >= VERBOSE_LOW) {
    std::cout << "\tInitial population created" << std::endl << std::endl;
  }

  //Begin loop
  int counter = 0;
  while(counter < max_iterations) {
    counter++;

    if(verbose >= VERBOSE_LOW) {
      std::cout << "\tIteration " << counter << "/" << max_iterations << std::endl;
    }

    /**
    * VARIATION
    *
    * Crossover - perform with the best chromosome and all other chromosomes
    * Mutation - perform mutations on the best item
    **/

    //Crossover
    if(verbose >= VERBOSE_MED) {
      std::cout << "\t\tBegin Crossover" << std::endl;
    }

    Chromosome* best= (*population.begin()).first;
    std::vector<std::pair<Chromosome*, double>> temp_vec;
    int temp_counter = 1;
    for(auto it2 = ++population.begin(); it2 != population.end(); ++it2) {
      if(verbose >= VERBOSE_HIGH) {
        std::cout << "\t\t\tCrossover " << temp_counter << std::endl;
      }
      temp_counter++;

      //Get a random index to split on
      int index = best->get_rand_index();

      //Allocate and create two Chromosome objects
      Chromosome* temp_c1 = new Chromosome(best, (*it2).first, index);
      Chromosome* temp_c2 = new Chromosome((*it2).first, best, index);

      //add them to the temporary vector so iteration is not screwed up
      temp_vec.push_back(std::make_pair(temp_c1, this->evaluator(temp_c1)));
      temp_vec.push_back(std::make_pair(temp_c2, this->evaluator(temp_c2)));
    }

    //insert all the values in the temp vec into the population
    for(int i = 0; i < temp_vec.size(); i++) {
      population.insert(temp_vec[i]);
    }

    if(verbose >= VERBOSE_MED) {
      std::cout << "\t\tCrossover complete, pop size: " << population.size() << std::endl;
    }

    //Mutation
    if(verbose >= VERBOSE_MED) {
      std::cout << "\t\tBegin Mutation" << std::endl;
    }

    for(int j = 0; j < mutate_count; j++) {
      if(verbose >= VERBOSE_HIGH) {
        std::cout << "\t\t\tMutate " << (j + 1) << std::endl; 
      }

      //Create a mutation of the best chromosome, add to the population
      Chromosome* temp_c = new Chromosome((*population.begin()).first, mutate_prob);
      population.insert(std::make_pair(temp_c,this->evaluator(temp_c)));
    }

    if(verbose >= VERBOSE_MED) {
      std::cout << "\t\tMutation complete, pop_size: " << population.size() << std::endl;
    }

    /**
    * UPDATE
    *
    * Trim to the population size
    */

    if(verbose >= VERBOSE_MED) {
      std::cout << "\t\tBegin Trimming" <<  std::endl;
    }

    //Create an iterator and advance to the index past the last in the best population
    auto it3 = population.begin();
    std::advance(it3, this->pop_size);

    //Iterate until end of set is found
    while (it3 != population.end()) {
      //Store the current iterator, post increment
      auto temp = it3++;

      //free allocated memory
      delete (*temp).first;

      //delete item from set
      population.erase(temp);
    }

    if(verbose >= VERBOSE_MED) {
      std::cout << "\t\tTrimming complete, pop_size: " << population.size() << std::endl;
    }

    if (verbose >= VERBOSE_LOW) {
       std::cout << "\tIteration "<< counter << "/" << max_iterations << " complete, min: " << (*population.begin()).second << std::endl << std::endl;
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

  if(verbose >= 1) {
    std::cout << "Finished in " << counter << " iterations, min val: " << (*population.begin()).second << std::endl;
  }

  //Get the best parameters
  std::vector<double> retval = (*population.begin()).first->get_params();

  //free the rest of the set
  for(auto it = population.begin(); it != population.end(); ++it) {
    delete (*it).first;
  }

  return retval;
}

//The Goldstein-Price algorithm
double GeneticAlgorithm::goldstein_price(Chromosome* c) {
  return (std::pow((*c)[0] + (*c)[1] + 1, 2) * (19 - 14 * (*c)[0] + 3 * std::pow((*c)[0],2) - 14 * (*c)[1] + 6 * (*c)[0] * (*c)[1] + 3 * std::pow((*c)[1],2)) + 1) * 
                                                      ((std::pow(2 * (*c)[0] - 3 * (*c)[1], 2) * 
                                                      (18 - 32 * (*c)[0] + 12 * std::pow((*c)[0], 2) + 48 * (*c)[1] - 36 * (*c)[0] * (*c)[1] + 27 * std::pow((*c)[1],2))) + 30);
}

//The banana algorithm
double GeneticAlgorithm::banana(Chromosome* c) {
  return std::pow(1 - (*c)[0], 2) + 100 * std::pow(((*c)[1] - std::pow((*c)[0], 2)), 2);
}

//The function to run a Genetic algorithm on the banana function and return the runtime
double GeneticAlgorithm::ga_banana(Chromosome* c) {
  //Seed with the chromosome's first parameter
  std::srand((*c)[0]);

  //create the GeneticAlgorithm object
  GeneticAlgorithm ga(Evaluation::BANANA, (*c)[1]);

  //run and clock
  std::clock_t ts = std::clock();

  //We scale down the mutate probability so mutations will actually occur
  //we are limimted to the same normalization limits for each parameter
  ga.run(GA_MAX_ITERS, VERBOSE_NONE, (*c)[2], ((*c)[3]/GA_MUTATE_PROB_CUT));      
  std::clock_t te = std::clock();                                                 
                                                                                  
  //return the runtime
  return ((float)te - (float)ts) / CLOCKS_PER_SEC;
}

//The function to run a Genetic algorithm on the Goldstein-price function and return the runtime
double GeneticAlgorithm::ga_goldstein_price(Chromosome* c) {
  //seed with the chromosome's first parameter
  std::srand((*c)[0]);

  //create the GeneticAlgorithm object
  GeneticAlgorithm ga(Evaluation::GOLDSTEIN_PRICE, (*c)[1]);

  //run and clock
  std::clock_t ts = std::clock();

  //We scale down the mutate probability so mutations will actually occur
  //we are limimted to the same normalization limits for each parameter
  ga.run(GA_MAX_ITERS, VERBOSE_NONE, (*c)[2], ((*c)[3]/GA_MUTATE_PROB_CUT));
  std::clock_t te = std::clock();

  return ((float)te - (float)ts) / CLOCKS_PER_SEC;

}

