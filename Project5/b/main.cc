#include "boost/program_options.hpp"
#include "chromosome.hh"
#include "ga.hh"
#include <iostream>
#include <random>
#include <time.h>

#define DEF_POP_SIZE 4

namespace po = boost::program_options;
using namespace ga;

int main(int argc, char** argv) {
  std::srand(std::time(NULL));

  int pop_size = DEF_POP_SIZE;
  po::options_description desc("Allowed Arguments");
  desc.add_options()
    ("help,h", "Display all arguments and their action")
    ("popsize,p", po::value<int>(&pop_size), "The size of the population to maintain")
    ("crossover,c", po::bool_switch()->default_value(false), "Perform crossover variation")
    ("mutation,m", po::bool_switch()->default_value(false), "Perform mutation variation")
    ("banana,b", po::bool_switch()->default_value(false), "Evaluate on the banana equation")
    ("goldstein,g", po::bool_switch()->default_value(false), "Evaluation on the goldstein-price equation");



  po::variables_map vm;
  po::store(po::parse_command_line(argc, argv, desc), vm);
  po::notify(vm);

  //Check for help
  if(vm.count("help")) {
    std::cout << desc << std::endl;
    std::exit(0);
  }

  Variation::Type var_type;
  Evaluation::Type eval_type;
  if (vm["crossover"].as<bool>() && vm["mutation"].as<bool>()) {
    std::cerr << "You cannot specify multiple variation types" << std::endl;
    std::exit(EXIT_FAILURE);
  }
  else if (vm["mutation"].as<bool>()) {
    var_type = Variation::MUTATION;
  }
  else {
    var_type = Variation::CROSSOVER;
  }


  if (vm["banana"].as<bool>() && vm["goldstein"].as<bool>()) {
    std::cerr << "You cannot specify multiple evaluation equations" << std::endl;
    std::exit(EXIT_FAILURE);
  }
  else if (vm["goldstein"].as<bool>()) {
    eval_type = Evaluation::BANANA;
  }
  else {
    eval_type = Evaluation::GOLDSTEIN_PRICE;
  }

  GeneticAlgorithm driver(eval_type, var_type, pop_size);
  driver.run();

  // std::cout << "Creating random chromosome" << std::endl;
  // Chromosome rand_test = Chromosome(2, 0, 1);
  // std::cout << "done" << std::endl;
  // double ri1 = rand_test[0];
  // double ri2 = rand_test[1];
  // std::cout << "rand_test[0]: " << ri1 << std::endl;
  // std::cout << "rand_test[1]: " << ri2 << std::endl <<std::endl;

  // std::vector<int> var_test(2, 5);
  // std::cout << "Creating known chromosome" << std::endl;
  // Chromosome known_test = Chromosome(var_test, 0, 1);
  // std::cout << "done" << std::endl;
  // double ki1 = known_test[0];
  // double ki2 = known_test[1];
  // std::cout << "known_test[0]: " << ki1 << std::endl;
  // std::cout << "known_test[1]: " << ki2 << std::endl;


}