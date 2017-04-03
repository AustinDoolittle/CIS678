###
# Project 4
# Main file for Python Neural Network
#
# Author: Austin Doolittle
###

import numpy as np
import argparse as ap
import sys
from os.path import splitext, basename
import Net as nn
import Dataset as ds
import pickle as pkl

#constants
DEF_MOMENTUM = .5
DEF_TIMEOUT = 750
DEF_TARGET = .001
DEF_BATCH = 10
DEF_DIVERGE = 5
DEF_INTER = 1
DEF_WEIGHTS_DIR = "Weights/"

#the main function to run the neural network on
def main(argv):
  #Parse the arguments provided from the commandline
  parser = ap.ArgumentParser(description="This is a neural network written in python using the numpy library for matrix operations")
  parser.add_argument("--hidden", nargs="*", type=int, help="The topology of the hidden layers of the network")
  parser.add_argument("-f", "--featurecount", required=True, type=int, help="The size of the feature vector to feed into the network")
  parser.add_argument("-k", "--classcount", required=True, type=int, help="The number of classes to classify with")
  parser.add_argument("--data", required=True, help="The file to pull data from")
  parser.add_argument("-m", "--momentum", default=DEF_MOMENTUM, type=float, help="The momentum constant to train with")
  parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Increase Verbosity of the program")
  parser.add_argument("--pca", default=False, action="store_true", help="Perform PCA on the dataset")
  parser.add_argument("--remcon", default=False, action="store_true", help="Remove constant values from the data")
  parser.add_argument("--timeout", default=DEF_TIMEOUT, type=int, help="Set the timeout of training")
  parser.add_argument("-t", "--target", default=DEF_TARGET, type=float, help="The target validation error to reach")
  parser.add_argument("--batch", default=DEF_BATCH, type=int, help="The batch size to train on")
  parser.add_argument("--weightfile", help="The pickle file to load weights from")
  parser.add_argument("-i", "--iterations", default=DEF_INTER, type=int, help="Number of times to pull data, train. Highest accuracy is found and weights are stored")
  parser.add_argument("--diverge", default=DEF_DIVERGE, type=int, help="The number of times the validation set and training set can diverge before training is ended")
  args = parser.parse_args()

  max_acc = 0
  max_weights = None

  #if we didn't provide a weightfile, iterate and train
  if args.weightfile is None:
    #iterate over provided iterations
    for i in xrange(args.iterations):
      print "Iteration " + str(i + 1)

      #generate dataset
      data = ds.Dataset(args.data, args.featurecount, args.classcount, remove_constants=args.remcon, perform_pca=args.pca)

      #create the topology of the neural network
      if args.hidden is not None:
        topology = np.append(data.train_set[0][0].shape[0], args.hidden)
      else:
        topology = np.array(data.train_set[0][0].shape[0])

      topology = np.append(topology, [data.train_set[0][-1].shape[0]])

      #create the Neural Network
      net = nn.Net(topology, args.momentum, args.verbose)

      #train the neural network until termination conditions are met
      net.train(data, args.target, args.batch, args.diverge, args.timeout, draw_graph=(args.iterations == 1))

      #test on validation set
      acc = net.test(data.val_set)

      #if we have a new max, store it
      if acc > max_acc:
        max_weights = net.weights
        max_acc = acc

    #print the max accuracy
    print "~~MAX ACC~~"
    print str(max_acc * 100) + "%"
    print "Saving Weights"

    #create the filename
    weights_file = basename(args.data)
    weights_file = splitext(weights_file)[0]
    temp_file = "_"
    if args.pca:
      temp_file += "pca_"
    if args.remcon:
      temp_file += "remcon_"
    weights_file = DEF_WEIGHTS_DIR + weights_file + temp_file + "weights"

    #save the weights
    np.save(weights_file, max_weights)

    #get a full dataset just for funsies
    data = ds.Dataset(args.data, args.featurecount, args.classcount, split=False, remove_constants=args.remcon, perform_pca=args.pca)

  else:
    #load the cached weights
    print "Pulling from weight file"
    try:
      max_weights = np.load(args.weightfile)
    except:
      print "Error loading weights"
      sys.exit(0)
    #get a full dataset
    data = ds.Dataset(args.data, args.featurecount, args.classcount, split=False, remove_constants=args.remcon, perform_pca=args.pca)

    #create the topology
    if args.hidden is not None:
      topology = np.append(data.train_set[0][0].shape[0], args.hidden)
    else:
      topology = np.array(data.train_set[0][0].shape[0])

    topology = np.append(topology, [data.train_set[0][-1].shape[0]])

  #create the final neural network
  net = nn.Net(topology, args.momentum, args.verbose)
  net.load_weights(max_weights)

  #get the total accuracy and print
  final_acc = net.test(data.train_set)
  print "Final accuracy over full data: " + str(final_acc * 100)

  

if __name__ == "__main__":
  #call main function
  main(sys.argv[1:])