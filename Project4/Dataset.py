import random
import numpy as np
from sklearn.feature_selection import VarianceThreshold

class Dataset(object):

  def __init__(self, filename, feature_count, class_count, remove_constants=False):
    try:
      with open(filename, 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    except:
      raise ValueError("The specified Dataset file could not be opened")

    if len(lines) == 0:
      raise ValueError("There are no lines in this Dataset file")

    self.feature_count = feature_count

    
    for line in lines:
      words = line.split()

      inputs = []
      for feat in words[:-1]:
        inputs.append(float(feat))

      if len(inputs) != self.feature_count:
        raise ValueError("The Dataset is formatted incorrectly. Expected " + str(self.feature_count) + " features, got " + str(len(inputs)))

      outputs = [1 if int(words[self.feature_count]) == x else 0 for x in range(0,class_count)]

      retval.append((np.array(inputs).reshape(len(inputs), 1), np.array(outputs).reshape(len(outputs), 1)))

    if remove
    
    vr = VarianceThreshold()

    retval = vr.fit_transform(retval)

    random.shuffle(retval)

    self.sets = np.array(retval)


  def __getitem__(self, key):
    if not isinstance(key, int):
      raise ValueError("Index must be an int, was given a " + str(type(key)))

    if key >= len(self.sets) or key < -len(self.sets):
      raise IndexError("Index " + str(key) + " is out of bounds")

    return self.sets[key]

  def __len__(self):
    return len(self.sets)

    
    
