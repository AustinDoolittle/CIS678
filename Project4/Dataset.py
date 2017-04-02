import random
import numpy as np
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA

class Dataset(object):

  def __init__(self, filename, feature_count, class_count, remove_constants=False, perform_pca=False):
    try:
      with open(filename, 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    except:
      raise ValueError("The specified Dataset file could not be opened")

    if len(lines) == 0:
      raise ValueError("There are no lines in this Dataset file")

    self.feature_count = feature_count

    input_arr = []
    output_arr = []
    for line in lines:
      words = line.split()

      inputs = []
      for feat in words[:-1]:
        inputs.append(float(feat))

      if len(inputs) != self.feature_count:
        raise ValueError("The Dataset is formatted incorrectly. Expected " + str(self.feature_count) + " features, got " + str(len(inputs)))

      outputs = [1 if int(words[self.feature_count]) == x else 0 for x in range(0,class_count)]

      input_arr.append(np.array(inputs))
      output_arr.append(np.array(outputs))

    if remove_constants:
    
      vr = VarianceThreshold()

      input_arr = vr.fit_transform(input_arr)

    if perform_pca:
      pca = PCA()
      input_arr = pca.fit_transform(input_arr)

    input_arr = [x.reshape(input_arr[0].shape[0], 1) for x in input_arr]
    output_arr = [x.reshape(output_arr[0].shape[0], 1) for x in output_arr]

    retval = zip(input_arr, output_arr)
    random.shuffle(retval)

    s1 = int(len(retval) *.75)
    s2 = int(len(retval) * .125)

    self.train_set = retval[:s1]
    self.test_set = retval[s1:s1+s2]
    self.val_set = retval[s1+s2:] 

    
    
