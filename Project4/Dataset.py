import random
import numpy as np

class Dataset(object):

  def __init__(self, filename, feature_count, class_count):
    try:
      with open(filename, 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    except:
      raise ValueError("The specified Dataset file could not be opened")

    if len(lines) == 0:
      raise ValueError("There are no lines in this Dataset file")

    self.feature_count = feature_count

    retval = []
    for line in lines:
      words = line.split()

      inputs = []
      for feat in words[:-1]:
        inputs.append(float(feat))

      if len(inputs) != self.feature_count:
        raise ValueError("The Dataset is formatted incorrectly. Expected " + str(self.feature_count) + " features, got " + str(len(inputs)))

      outputs = [1 if words[self.feature_count] == x else 0 for x in range(0,class_count)]

      retval.append((np.array(inputs), np.array(outputs)))
    random.shuffle(retval)

    self.sets = np.array(retval)


  def __getitem__(self, key):
    if not isinstance(key, int):
      raise ValueError("Index must be an int, was given a " + str(type(key)))

    if key >= len(self.sets) or key < -len(self.sets):
      raise IndexError("Index " + str(key) + " is out of bounds")

    return self.sets[key]

    
    
