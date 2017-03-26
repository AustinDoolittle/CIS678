import numpy as np
import time
import Dataset
import math

DEF_TRAIN_RATE = 0.5
DEF_MOMENTUM = 0.5

class Net(object):
  def __init__(self, topology, momentum=DEF_MOMENTUM, verbose=False):
    if len(topology) < 2:
      raise ValueError("The topology of the neural network must be at least 2 values long")

    self.train_rate = DEF_TRAIN_RATE
    self.featurecount = topology[0]
    self.classcount = topology[-1]
    self.verbose = verbose

    temp_weights = []
    temp_del_weights = []
    temp_layers = []

    for l in range(0, len(topology)-1):
      temp_weights.append(np.random.uniform(low=-0.01, 
                                            high=0.01, 
                                            size=(topology[l]+1, topology[l+1])))
      temp_del_weights.append(np.zeros((topology[l]+1, topology[l+1])))
      temp_layers.append(np.zeros(topology[l] + 1))

    temp_layers.append(np.zeros(topology[l]))

    self.layers = np.array(temp_layers)
    self.weights = np.array(temp_weights)
    self.del_weights = np.array(temp_del_weights)

  def activate(x):
    return 1/(1+math.exp(-x))

  def train(self, train_set, test_set, target, interval, diverge_count, timeout):
    start_time = time.localtime()
    test_index = 0 
    prev_diff = 0
    diverge_count = 0

    counter = 0
    val_counter = 1
    prev_weights = self.weights
    prev_del_weights = self.del_weights

    while True:
      if self.verbose:
        print "Training " + str(counter)

      tr_avg = 0
      prev_err = .5

      for i in range(0, interval):
        error_sum = 0
        for j in range(0, len(train_set)):
          res = forward(train_set[j][0])
          if self.verbose:
            print "\tOutputs/Expected"
            for k in range(0, len(res)):
              print "\t\t" + str(res[k]) + "/" + str(train_set[j][1][k])
          err = get_error(res, train_set[j][1])
          if self.verbose:
            print "\tError: " + str(err)

          error_sum += err

          back_prop


  def forward(self, inputs):
    self.layers[0] = inputs

    for i in range(1, len(layers)):
      if i != len(layers - 1):
        layers[i][1:] = weights[i-1].transpose() * layers[i-1]
      else:
        layers[i] = weights[i-1].transpose() * layers[i-1]

      activate(layers[i])
    return layers[-1]

  def get_error(self, actual, expected):
    return np.sum(np.square(expected - actual)) / len(expected)

  def back_prop(self, expected):
    




