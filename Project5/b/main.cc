/**
* main.cc
*
* Contains the main method to run the GeneticAlgorithm class
* Author: Austin Doolittle
**/

#include "boost/program_options.hpp"
#include "chromosome.hh"
#include "ga.hh"
#include <iostream>
#include <stdlib.h>
#include <time.h>
// #include <string>

//Define constants
#define DEF_POP_SIZE 4
#define DEF_MUTATE_PROB 10
#define DEF_MAX_ITERS 10000

//setup namespaces
namespace po = boost::program_options;
using namespace ga;

//main method
int main(int argc, char** argv) {

  //declare variables to store arguments in
  int pop_size = DEF_POP_SIZE;
  int max_iterations = DEF_MAX_ITERS;
  int verbose_level = VERBOSE_NONE;
  int seed = (int)std::time(NULL);
  int mutate_prob = DEF_MUTATE_PROB;

  //Create argument dictionary
  po::options_description desc("Allowed Arguments");
  desc.add_options()
    ("help,h", "Display all arguments and their description")
    ("popsize,p", po::value<int>(&pop_size), "The size of the population to maintain")
    ("banana,b", po::bool_switch()->default_value(false), "Evaluate on the banana equation")
    ("goldstein,g", po::bool_switch()->default_value(false), "Evaluate on the goldstein-price equation")
    ("iterations,i", po::value<int>(&max_iterations), "The maximum iterations to run")
    ("inception", po::bool_switch()->default_value(false), "Use a Genetic Algorithm to determine optimal parameters for the given evaluation type")
    ("seed", po::value<int>(&seed), "The value to seed random generation with")
    ("mprob", po::value<int>(&mutate_prob), "The probability of mutation, (1/n probability where n is value entered)")
    ("mcount", po::value<int>(), "The number of mutations to perform")
    ("verbose,v", po::value<int>(&verbose_level), "Increase verbosity (1 = low, 2 = medium, 3 = high)");
  po::variables_map vm;
  po::store(po::parse_command_line(argc, argv, desc), vm);
  po::notify(vm);

  //Check for help
  if(vm.count("help")) {
    std::cout << desc << std::endl;
    std::exit(0);
  }

  //seed the random generator with the given value
  std::srand(seed);

  //get the mutate count, default to the population size
  int mutate_count = 0;
  if (vm.count("mcount")) {
    mutate_count = vm["mcount"].as<int>();
  }
  else {
    mutate_count = pop_size;
  }

  //Get the evaluation type, default to banana
  Evaluation::Type eval_type;
  if (vm["banana"].as<bool>() && vm["goldstein"].as<bool>()) {
    std::cerr << "You cannot specify multiple evaluation equations" << std::endl;
    std::exit(EXIT_FAILURE);
  }
  else if (vm["goldstein"].as<bool>()) {
    //check for GA on GA
    if (vm["inception"].as<bool>()) {
      eval_type = Evaluation::GA_GOLDSTEIN_PRICE;
    }
    else  {
      eval_type = Evaluation::GOLDSTEIN_PRICE;
    }
  }
  else {
    //check for GA on GA
    if (vm["inception"].as<bool>()) {
      eval_type = Evaluation::GA_BANANA;
    }
    else  {
      eval_type = Evaluation::BANANA;
    }
  }

  //create genetic algorithm object
  GeneticAlgorithm driver(eval_type, pop_size);

  //run and clock
  std::cout << "Starting Genetic Algorithm..." << std::endl;
  std::clock_t ts = std::clock();
  std::vector<double> vars = driver.run(max_iterations, verbose_level, mutate_prob, mutate_count);
  std::clock_t te = std::clock();

  //print optimal variables
  std::cout << "Variables: ";
  for(int i = 0; i < vars.size(); i++) {
    if(i != 0) {
      std::cout << ", ";
    }
    std::cout << i << ": " << vars[i];
  }
  std::cout << std::endl;

  //print runtime
  std::cout << "runtime: " << ((float)te - (float)ts) / CLOCKS_PER_SEC << std::endl;
}