###
# Project 4
# The file containing the neural network class
#
# Author: Austin Doolittle
###

import numpy as np
import timeit
import Dataset
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


#define constants
DEF_TRAIN_RATE = 0.5
DEF_MOMENTUM = 0.5
DEF_VAL_SIZE = 50

#the Neural Network object
class Net(object):

  #init the Neural Network
  def __init__(self, topology, momentum=DEF_MOMENTUM, verbose=False):
    if len(topology) < 2:
      raise ValueError("The topology of the neural network must be at least 2 values long")

    #set the class variables
    self.train_rate = DEF_TRAIN_RATE
    self.featurecount = topology[0]
    self.classcount = topology[-1]
    self.verbose = verbose
    self.momentum = momentum

    temp_weights = []
    temp_del_weights = []
    temp_layers = []

    #set up the layers, weights, and delta weights
    for l in xrange(0, len(topology)-1):
      temp_weights.append(np.random.uniform(low=-0.01, 
                                            high=0.01, 
                                            size=(topology[l]+1, topology[l+1])))
      temp_del_weights.append(np.zeros((topology[l]+1, topology[l+1])))
      temp_layers.append(np.ones((topology[l] + 1, 1)))

    temp_layers.append(np.ones((topology[l], 1)))

    #convert to numpy arrays and store as class variables
    self.layers = np.array(temp_layers)
    self.weights = np.array(temp_weights)
    self.del_weights = np.array(temp_del_weights)

  #sigmoid activation function
  def activate(self, x):
    return 1/(1+np.exp(-x))

  #backpropogation over the neural network
  def backprop(self, expected):
    #get the gradients on the output layer
    gradients = (expected - self.layers[-1]) * self.layers[-1] * (1 - self.layers[-1])

    #iterate over the network backwards
    for i in reversed(xrange(self.layers.shape[0] - 1)):
      #get the change in weights
      self.del_weights[i] = (self.train_rate * np.dot(self.layers[i], gradients.transpose())) + (self.momentum * self.del_weights[i])

      #apply the change in weights
      self.weights[i] += self.del_weights[i]

      #get the gradients for the current layer
      gradients = np.dot(self.weights[i][1:, :], gradients) * ((1 - self.layers[i][1:]) * self.layers[i][1:])

  #the full training method that trains in batches until the termination conditions are met
  def train(self, data, target, batch_size, diverge_limit, timeout, draw_graph=True):
    #set local variables used over training
    train_start = timeit.default_timer()
    test_index = 0 
    prev_diff = 0
    diverge_count = 0
    counter = 0
    plot_counter = 0
    val_counter = 1
    prev_weights = self.weights
    prev_del_weights = self.del_weights
    plot_tr_err_X = []
    plot_tr_err_Y = []
    plot_test_err_X = []
    plot_test_err_Y = []

    #loop until termination conditions are met
    while True:
      if self.verbose:
        print "Training " + str(counter)

      tr_avg = 0
      prev_err = .5

      #train over the batch size
      for i in xrange(0, batch_size):
        error_sum = 0
        plot_counter += 1

        #train one epoch
        for j in xrange(0, len(data.train_set)):
          res = self.forward(data.train_set[j][0])

          if self.verbose:
            print "\tOutputs/Expected"
            for k in xrange(0, len(res)):
              print "\t\t" + str(res[k]) + "/" + str(data.train_set[j][1][k])

          #get the error of the outputs
          err = self.get_error(res, data.train_set[j][1])
          if self.verbose:
            print "\tError: " + str(err)

          #add to the sum
          error_sum += err
          #backprop over the errors
          self.backprop(data.train_set[j][1])

        #get the average training error
        tr_avg = error_sum / len(data.train_set)

        plot_tr_err_X.append(plot_counter)
        plot_tr_err_Y.append(tr_avg)

        #check for improvement, adjust the train rate
        if tr_avg < prev_err:
          #we improved, increase train rate
          self.train_rate *= 1.05
          prev_weights = self.weights
          prev_del_weights = self.del_weights
        else:
          #we did not improve, decrease train rate and rollback weights
          self.train_rate *= .5
          self.weights = prev_weights
          self.del_weights = prev_del_weights

        prev_err = tr_avg
        counter += 1

      if self.verbose:
        print "Testing..."

      #validate on the test data
      val_avg = 0
      # for i in xrange(DEF_VAL_SIZE):
      #   res = self.forward(data.val_set[test_index][0])
      #   val_avg += self.get_error(res, data.val_set[test_index][1])
      #   test_index = (test_index + 1) % len(data.test_set)
      # val_avg /= DEF_VAL_SIZE

      for i in xrange(len(data.val_set)):
        res = self.forward(data.val_set[test_index][0])
        val_avg += self.get_error(res, data.val_set[test_index][1])
        test_index = (test_index + 1) % len(data.test_set)
      val_avg /= len(data.val_set)

      plot_test_err_X.append(plot_counter)
      plot_test_err_Y.append(val_avg)

      #get the difference
      diff = val_avg - tr_avg

      #test termination conditions
      if val_avg <= target:
        #done!
        print "~TARGET REACHED~"
        print "Error: " + str(val_avg)
        break
      else:
        #print the validation info
        print  "\tValidate " + str(val_counter) + ", Train Err: " + str(tr_avg) + ", Val Err: " + str(val_avg) + ", Diff: " + str(diff) + ", Target: " + str(target)
        val_counter += 1

      #check for divergence
      if diff >= prev_diff:
        diverge_count += 1
        if diverge_count == diverge_limit:
          print "~DIVERGE LIMIT~"
          break
      else:
        diverge_count = 0

      prev_diff = diff

      #check for timeout
      train_end = timeit.default_timer()
      if train_end - train_start > timeout:
        print "~TIMEOUT~"
        break
    
    if draw_graph:
      #plot the training graph
      max_y = max(max(plot_test_err_Y), max(plot_tr_err_Y))
      max_y += max_y * .25
      plt.axis([0, plot_counter, 0, max_y])
      plt.plot(plot_tr_err_X, plot_tr_err_Y, 'r', plot_test_err_X, plot_test_err_Y, 'b')
      train_plot_legend = mpatches.Patch(color='red', label="Train Error")
      test_plot_legend = mpatches.Patch(color='blue', label="Validation Error")
      plt.legend(handles=[train_plot_legend, test_plot_legend])
      plt.title("Training Error")
      plt.xlabel("Epochs")
      plt.ylabel("Error (MSQ)")
      plt.show()

  #test one instance of data
  def test_one(self, line):
    #feed forward
    res = self.forward(line[0])
    if self.verbose:
      print "Output/Expected:"
      for i in xrange(0, len(res)):
        print "\t" + str(res[i]) + "/" + str(line[1][i])

    #get max index
    max_expected = np.argmax(line[1])
    max_res = np.argmax(res)

    #return True if we were right, False if not
    return max_res == max_expected

  #Test over the test set
  def test(self, test_set):
    total_count = len(test_set)
    correct = 0

    #iterate over every training instance
    for i in xrange(0, total_count):
      if self.verbose:
        print "Testing " + str(i)

      #test one and see if we were right
      if self.test_one(test_set[i]):
        correct += 1
        if self.verbose:
          print "Correct: " + str(correct) + "/" + str(total_count)
      elif self.verbose:
        print "Incorrect: " + str(correct) + "/" + str(total_count)

    #print results
    print "\n~~ RESULTS ~~"
    print str(correct) + "/" + str(total_count) + " correct, " + str((correct + 0.0)/total_count * 100) + "% Accuracy\n"
    return (correct + 0.0)/total_count;


  #feed forward method
  def forward(self, inputs):
    #load inputs
    self.layers[0][1:] = inputs

    #iterate over layers, propogate forward
    for i in xrange(1, len(self.layers)):
      #if we are not on the last layer, only set the slices to prevent
      #overriding the bias node
      if i != len(self.layers) - 1:
        self.layers[i][1:] = np.dot(self.weights[i-1].transpose(), self.layers[i-1])
        self.layers[i][1:] = self.activate(self.layers[i][1:])
      else:
        self.layers[i] = np.dot(self.weights[i-1].transpose(), self.layers[i-1])
        self.layers[i] = self.activate(self.layers[i])

    return self.layers[-1]

  #calculate the MSQ on outputs
  def get_error(self, actual, expected):
    return np.sum(np.square(expected - actual)) / len(expected)

  #loads the weights from a np.array into the class weights
  def load_weights(self, weights):
    self.weights = weights

    




