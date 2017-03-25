import numpy as np
import argparse as ap
import sys
import Net as NN

def main(argv):
  parser = ap.ArgumentParser(description="This is a neural network written in python using the numpy library for matrix operations")
  parser.add_argument("--hidden", nargs="*", type=int, help="The topology of the hidden layers of the network")
  parser.add_argument("-f", "--featurecount", required=True, type=int, help="The size of the feature vector to feed into the network")
  parser.add_argument("-k", "--classcount", required=True, type=int, help="The number of classes to classify with")
  parser.add_argument("--trainfile", required=True, help="The file to pull training data from")
  parser.add_argument("--testfile", required=True, help="The file to pull testing data from")
  args = parser.parse_args()

  if args.hidden is not None:
    topology = np.append([args.featurecount], args.hidden)
  else:
    topology = np.array(args.featurecount)

  topology = np.append(topology, [args.classcount])

  net = NN.Net(topology)

  print net.layers
  print net.weights
  print net.del_weights

  

if __name__ == "__main__":
  main(sys.argv[1:])