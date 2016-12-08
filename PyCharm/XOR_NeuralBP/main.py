from matplotlib.mlab import frange
from pybrain import SigmoidLayer, LinearLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
import matplotlib.pyplot as plt

dataSet = SupervisedDataSet(1, 1)
for i in range(10):
	dataSet.addSample(i, i*i)

Network = buildNetwork(dataSet.indim, 4, 1, hiddenclass=SigmoidLayer, outclass=LinearLayer, bias=True)

trainer = BackpropTrainer(Network, dataSet, learningrate=0.0001, momentum=0.01)
trainer.trainEpochs(10000)

x = []
y = []

for i in range(0, 10):
	y.append(Network.activate([i])[0])
for i in range(len(y)):
	x.append(i)

plt.plot(x, y)
plt.show()