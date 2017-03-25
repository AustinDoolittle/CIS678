import numpy as np

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





