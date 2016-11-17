from pybrain.datasets.classification import ClassificationDataSet
# below line can be replaced with the algorithm of choice e.g.
# from pybrain.optimization.hillclimber import HillClimber
from pybrain.optimization.populationbased.ga import GA
from pybrain.tools.shortcuts import buildNetwork

# create XOR dataset
d = ClassificationDataSet(2)
d.addSample([0., 0.], [0.])
d.addSample([0., 1.], [1.])
d.addSample([1., 0.], [1.])
d.addSample([1., 1.], [0.])
d.setField('class', [ [0.],[1.],[1.],[0.]])

nn = buildNetwork(2, 3, 1)
# d.evaluateModuleMSE takes nn as its first and only argument
print(nn.params)
nn._setParameters([ 1.27735382, -0.99438574, -0.10038079,  0.59488621 ,-0.15990679 ,-0.27051878,
 -0.00832801 , 0.90143745, -1.90395467, -0.63921904 -2.41466853,  1.55855459,
 -1.42786902])
print(nn.params)
nn.activate([11,11])