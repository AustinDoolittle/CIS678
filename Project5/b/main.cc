#include "boost/program_options.hpp"
#include "chromosome.hh"
#include "ga.hh"
#include <iostream>
#include <random>
#include <time.h>
#include <string>

#define DEF_POP_SIZE 4
#define DEF_MAX_ITERS 10000

namespace po = boost::program_options;
using namespace ga;

int main(int argc, char** argv) {
  int pop_size = DEF_POP_SIZE;
  int max_iterations = DEF_MAX_ITERS;
  int verbose_level = VERBOSE_NONE;
  int seed = (int)std::time(NULL);
  po::options_description desc("Allowed Arguments");
  desc.add_options()
    ("help,h", "Display all arguments and their action")
    ("popsize,p", po::value<int>(&pop_size), "The size of the population to maintain)")
    ("banana,b", po::bool_switch()->default_value(false), "Evaluate on the banana equation")
    ("goldstein,g", po::bool_switch()->default_value(false), "Evaluation on the goldstein-price equation")
    ("iterations,i", po::value<int>(&max_iterations), "The maximum iterations to run")
    ("inception", po::bool_switch()->default_value(false), "Use a Genetic Algorithm to determine optimal parameters for the given evaluation type")
    ("seed", po::value<int>(&seed), "The value to seed random generation with")
    ("verbose,v", po::value<int>(&verbose_level), "Increase verbosity");

  po::variables_map vm;
  po::store(po::parse_command_line(argc, argv, desc), vm);
  po::notify(vm);

  //Check for help
  if(vm.count("help")) {
    std::cout << desc << std::endl;
    std::exit(0);
  }

  std::srand(seed);

  Evaluation::Type eval_type;
  if (vm["banana"].as<bool>() && vm["goldstein"].as<bool>()) {
    std::cerr << "You cannot specify multiple evaluation equations" << std::endl;
    std::exit(EXIT_FAILURE);
  }
  else if (vm["goldstein"].as<bool>()) {
    if (vm["inception"].as<bool>()) {
      eval_type = Evaluation::GA_GOLDSTEIN_PRICE;
    }
    else  {
      eval_type = Evaluation::GOLDSTEIN_PRICE;
    }
  }
  else {
    if (vm["inception"].as<bool>()) {
      eval_type = Evaluation::GA_BANANA;
    }
    else  {
      eval_type = Evaluation::BANANA;
    }
  }

  GeneticAlgorithm driver(eval_type, pop_size);

  std::clock_t ts = std::clock();
  std::vector<double> vars = driver.run(max_iterations, verbose_level);
  std::clock_t te = std::clock();

  std::cout << "Variables: ";
  for(int i = 0; i < vars.size(); i++) {
    if(i != 0) {
      std::cout << ", ";
    }
    std::cout << i << ": " << vars[i];
  }
  std::cout << std::endl;
  std::cout << "runtime: " << ((float)te - (float)ts) / CLOCKS_PER_SEC << std::endl;


}