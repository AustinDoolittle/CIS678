import numpy as np
import timeit
import Dataset
import math

DEF_TRAIN_RATE = 0.5
DEF_MOMENTUM = 0.5
DEF_VAL_batch_sizeS = 10

class Net(object):
  def __init__(self, topology, momentum=DEF_MOMENTUM, verbose=False):
    if len(topology) < 2:
      raise ValueError("The topology of the neural network must be at least 2 values long")

    self.train_rate = DEF_TRAIN_RATE
    self.featurecount = topology[0]
    self.classcount = topology[-1]
    self.verbose = verbose
    self.momentum = momentum

    temp_weights = []
    temp_del_weights = []
    temp_layers = []

    for l in xrange(0, len(topology)-1):
      temp_weights.append(np.random.uniform(low=-0.01, 
                                            high=0.01, 
                                            size=(topology[l]+1, topology[l+1])))
      temp_del_weights.append(np.zeros((topology[l]+1, topology[l+1])))
      temp_layers.append(np.ones((topology[l] + 1, 1)))

    temp_layers.append(np.ones((topology[l], 1)))

    self.layers = np.array(temp_layers)
    self.weights = np.array(temp_weights)
    self.del_weights = np.array(temp_del_weights)

  def activate(self, x):
    return 1/(1+np.exp(-x))

  def backprop(self, expected):
    gradients = (expected - self.layers[-1]) * self.layers[-1] * (1 - self.layers[-1])

    for i in reversed(xrange(self.layers.shape[0] - 1)):
      self.del_weights[i] = (self.train_rate * np.dot(self.layers[i], gradients.transpose())) + (self.momentum * self.del_weights[i])

      self.weights[i] += self.del_weights[i]
      gradients = np.dot(self.weights[i][1:, :], gradients) * ((1 - self.layers[i][1:]) * self.layers[i][1:])

  def train(self, data, target, batch_size, diverge_limit, timeout):
    train_start = timeit.default_timer()
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

      for i in xrange(0, batch_size):
        error_sum = 0
        for j in xrange(0, len(data.train_set)):
          res = self.forward(data.train_set[j][0])

          if self.verbose:
            print "\tOutputs/Expected"
            for k in xrange(0, len(res)):
              print "\t\t" + str(res[k]) + "/" + str(data.train_set[j][1][k])
          err = self.get_error(res, data.train_set[j][1])
          if self.verbose:
            print "\tError: " + str(err)

          error_sum += err

          self.backprop(data.train_set[j][1])

        tr_avg = error_sum / len(data.train_set)

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
      for i in xrange(0, batch_size):
        res = self.forward(data.val_set[test_index][0])
        val_avg += self.get_error(res, data.val_set[test_index][1])
        test_index = (test_index + 1) % len(data.test_set)
      val_avg /= batch_size

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

      train_end = timeit.default_timer()
      if train_end - train_start > timeout:
        print "~TIMEOUT~"
        break

  def test_one(self, line):
    res = self.forward(line[0])
    if self.verbose:
      print "Output/Expected:"
      for i in xrange(0, len(res)):
        print "\t" + str(res[i]) + "/" + str(line[1][i])

    #get max index
    max_expected = np.argmax(line[1])
    max_res = np.argmax(res)

    return max_res == max_expected

  def test(self, test_set):
    total_count = len(test_set)
    correct = 0
    for i in xrange(0, total_count):
      if self.verbose:
        print "Testing " + str(i)

      if self.test_one(test_set[i]):
        correct += 1
        if self.verbose:
          print "Correct: " + str(correct) + "/" + str(total_count)
      elif self.verbose:
        print "Incorrect: " + str(correct) + "/" + str(total_count)

    print "\n\n~~ RESULTS ~~"
    print str(correct) + "/" + str(total_count) + " correct, " + str((correct + 0.0)/total_count * 100) + "% Accuracy"
    return (correct + 0.0)/total_count;


  def forward(self, inputs):
    self.layers[0][1:] = inputs

    for i in xrange(1, len(self.layers)):
      if i != len(self.layers) - 1:
        self.layers[i][1:] = np.dot(self.weights[i-1].transpose(), self.layers[i-1])
        self.layers[i][1:] = self.activate(self.layers[i][1:])
      else:
        self.layers[i] = np.dot(self.weights[i-1].transpose(), self.layers[i-1])
        self.layers[i] = self.activate(self.layers[i])

    return self.layers[-1]

  def get_error(self, actual, expected):
    return np.sum(np.square(expected - actual)) / len(expected)

    




