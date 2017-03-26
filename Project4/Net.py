import numpy as np
import time
import Dataset
import math

DEF_TRAIN_RATE = 0.5
DEF_MOMENTUM = 0.5
DEF_VAL_INTERVALS = 10

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

  def activate(self, x):
    return 1/(1+math.exp(-x))

  def backprop(self, expected):
    gradients = (expected - self.layers[-1]) ** self.layers[-1] ** (1 - self.layers[-1])

    for i in reversed(range(0, len(layers) - 2)):
      self.del_weights[i] = (self.train_rate * (self.layers[i] * gradients.transpose())) + (self.momentum * self.del_weights[i])

      self.weights[i] += self.del_weights[i]
      gradients = (self.weights[i][1:, :] * gradients) ** (1 - (self.weights[i][1:, :] * gradients))

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

          back_prop(train_set[j][1])

        tr_avg = error_sum / len(train_set)

        if tr_avg < prev_err:
          self.train_rate *= 1.05
          prev_weights = self.weights
          prev_del_weights = self.del_weights
        else:
          self.train_rate *= .5
          self.weights = prev_weights
          self.del_weights = prev_del_weights

        prev_err = tr_avg
        counter += 1

      if self.verbose:
        print "Testing..."

      val_avg = 0
      for i in range(0, DEF_VAL_INTERVALS):
        res = forward(test_set[test_index][0])
        val_avg += get_error(res, test_set[test_index][1])
        test_index = (test_index + 1) % len(test_set)
      val_avg /= DEF_VAL_INTERVALS

      diff = tr_avg - val_avg

      #test termination conditions
      if val_avg <= target:
        print "~TARGET REACHED~"
        break
      else:
        print  "\tValidate " + str(val_counter) + ", Train Err: " + str(tr_avg) + ", Val Err: " + str(val_avg) + ", Diff: " + str(diff) + ", Target: " + str(target)
        val_counter += 1

      if diff < prev_diff:
        diverge_count += 1
        if diverge_count == diverge_limit:
          print "~DIVERGE LIMIT~"
          break
      else:
        diverge_count = 0

      prev_diff = diff

      train_end = time.localtime()
      if train_end - train_start > timeout:
        print "~TIMEOUT~"
        break

  def test(self, test_set):
    


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

    




