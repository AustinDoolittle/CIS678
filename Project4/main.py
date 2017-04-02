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
  parser.add_argument("--data", required=True, help="The file to pull data from")
  parser.add_argument("-m", "--momentum", default=DEF_MOMENTUM, type=float, help="The momentum constant to train with")
  parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Increase Verbosity of the program")
  parser.add_argument("--pca", default=False, action="store_true", help="Perform PCA on the dataset")
  parser.add_argument("--remcon", default=False, action="store_true", help="Remove constant values from the data")
  parser.add_argument("--timeout", default=DEF_TIMEOUT, type=int, help="Set the timeout of training")
  parser.add_argument("-t", "--target", default=DEF_TARGET, type=float, help="The target validation error to reach")
  parser.add_argument("--batch", default=DEF_BATCH, type=int, help="The batch size to train on")
  parser.add_argument("--diverge", default=DEF_DIVERGE, type=int, help="The number of times the validation set and training set can diverge before training is ended")
  args = parser.parse_args()

  data = ds.Dataset(args.data, args.featurecount, args.classcount, remove_constants=args.remcon, perform_pca=args.pca)

  if args.hidden is not None:
    topology = np.append(data.train_set[0][0].shape[0], args.hidden)
  else:
    topology = np.array(data.train_set[0][0].shape[0])

  topology = np.append(topology, [data.train_set[0][-1].shape[0]])

  net = nn.Net(topology, args.momentum, args.verbose)

  net.train(data, args.target, args.batch, args.diverge, args.timeout)

  acc = net.test(data.val_set)
  

if __name__ == "__main__":
  main(sys.argv[1:])