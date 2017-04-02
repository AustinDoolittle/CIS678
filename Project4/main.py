import numpy as np
import argparse as ap
import sys
import Net as nn
import Dataset as ds

DEF_MOMENTUM = .5
DEF_TIMEOUT = 750
DEF_TARGET = .001
DEF_BATCH = 10
DEF_DIVERGE = 5

def main(argv):
  parser = ap.ArgumentParser(description="This is a neural network written in python using the numpy library for matrix operations")
  parser.add_argument("--hidden", nargs="*", type=int, help="The topology of the hidden layers of the network")
  parser.add_argument("-f", "--featurecount", required=True, type=int, help="The size of the feature vector to feed into the network")
  parser.add_argument("-k", "--classcount", required=True, type=int, help="The number of classes to classify with")
  parser.add_argument("--trainfile", required=True, help="The file to pull training data from")
  parser.add_argument("--testfile", required=True, help="The file to pull testing data from")
  parser.add_argument("-m", "--momentum", default=DEF_MOMENTUM, type=float, help="The momentum constant to train with")
  parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Increase Verbosity of the program")
  parser.add_argument("--timeout", default=DEF_TIMEOUT, type=int, help="Set the timeout of training")
  parser.add_argument("-t", "--target", default=DEF_TARGET, type=float, help="The target validation error to reach")
  parser.add_argument("--batch", default=DEF_BATCH, type=int, help="The batch size to train on")
  parser.add_argument("--diverge", default=DEF_DIVERGE, type=int, help="The number of times the validation set and training set can diverge before training is ended")
  args = parser.parse_args()

  if args.hidden is not None:
    topology = np.append([args.featurecount], args.hidden)
  else:
    topology = np.array(args.featurecount)

  topology = np.append(topology, [args.classcount])

  # if args.hidden is not None:
  #   topology = np.append(train_set[0][0].shape[0], args.hidden)
  # else:
  #   topology = np.array(train_set[0][0].shape[0])

  # topology = np.append(topology, [train_set[0][-1].shape[0]])

  net = nn.Net(topology, args.momentum, args.verbose)

  train_set = ds.Dataset(args.trainfile, args.featurecount, args.classcount)
  test_set = ds.Dataset(args.testfile, args.featurecount, args.classcount)

  net.train(train_set, test_set, args.target, args.batch, args.diverge, args.timeout)

  acc = net.test(test_set)
  

if __name__ == "__main__":
  main(sys.argv[1:])