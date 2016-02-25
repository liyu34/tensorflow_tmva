import numpy as np
import tensorflow as tf

import classification.knn.knn as knn
import preprocessing.data_set
import preprocessing.ttree
import ROOT

signal = ROOT.TNtuple("ntuple", "ntuple", "x:y:z")
background = ROOT.TNtuple("ntuple", "ntuple", "x:y:z")
for i in range(10000):
    signal.Fill(ROOT.gRandom.Gaus(1, 20), ROOT.gRandom.Gaus(
        1, 20), ROOT.gRandom.Gaus(1, 20))
    background.Fill(ROOT.gRandom.Gaus(-1, 20),
                    ROOT.gRandom.Gaus(-1, 20), ROOT.gRandom.Gaus(-1, 20))


data = preprocessing.ttree.ttrees_to_internal(
    [signal, background], ["x", "y", "z"], binary=False)

test = np.array([[0., 0., 0.]])

scales = knn.scale(data.data(), 0.9)

train_tensor, labels_tensor, test_tensor, neighbours, d = knn.model_single(
    3, 2, 0.9, scales, 100)

sess = tf.Session()

print("Searching for 100 nearest neighbours")

results = sess.run(neighbours,
                   feed_dict={train_tensor: data.data(),
                              labels_tensor: data.labels(), test_tensor: test})
print("Signal neighbours: %d" % results[0])
print("Background neighbours: %d" % results[1])