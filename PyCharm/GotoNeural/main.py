from pybrain import TanhLayer, SoftmaxLayer
from pybrain.structure.modules.sigmoidlayer import SigmoidLayer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import random

features = []
featuresRandom = []

# Reading training data
def ReadFeatures():
    print("Reading features...\n ")
    prefeatures = []
    file = open('/media/sf_Python/PyCharm/GotoNeural/features.csv', 'r')
    for str in file:
        prefeatures.append(str.split(','))
    del(prefeatures[0])

    for prefeature in prefeatures:
        unitsDouble = []
        for sub in prefeature:
            unitsDouble.append(float(sub))
        del(unitsDouble[0])
        features.append(unitsDouble)

if __name__ == "__main__":
    random.seed();
    ReadFeatures()
    print("All features read.\n ")
    dataSet = SupervisedDataSet(len(features[0]) - 2, 1)
    for feature in features:
        dataSet.addSample(feature[:len(feature) - 2], feature[len(feature) - 1])

    Network = buildNetwork(dataSet.indim, 6, 1, hiddenclass=SigmoidLayer, outclass=SigmoidLayer)
    trainer = BackpropTrainer(Network, dataSet, learningrate=0.00005, momentum=0.00005)

    # Leaving 50/50 positives/negatives
    positives = negatives = 0
    for feature in features:
        if feature[len(feature)-1] == 0:
            negatives+=1
        else:
            positives+=1
    myi = 0
    while positives != negatives:
        if features[myi][len(features[myi])-1] == 0:
            del(features[myi])
            negatives-=1
        else:
            myi+=1

    # Random mix
    featuresSize = len(features)
    for i in range(featuresSize):
        featuresRandom.append([])
    myi = 0
    while len(features) != 0:
        rand = int(random.random()*10000%featuresSize)
        if featuresRandom[rand] == []:
            featuresRandom[rand] = features[myi]
            del features[myi]
    features = featuresRandom

    while True:
        TP = TN = FP = FN = 0
        error = 0
        for feature in features:
            output = Network.activate(feature[:dataSet.indim])

            answer = output[0] > 0.5
            rightAnswer = feature[len(feature)-1]
            error += rightAnswer - output[0]
            if answer:
                if rightAnswer:
                    TP+=1
                else:
                    FP+=1
            else:
                if rightAnswer:
                    FN+=1
                else:
                    TN+=1

        recall = (TP / (TP + FN)) if ((TP + FN) != 0) else 0
        precision = (TP / (TP + FP)) if ((TP + FP) != 0) else 0
        F_measure = 2 * ((precision * recall) / (precision + recall)) if (precision + recall != 0) else 0
        print("Precision: ", precision, ",", " Recall: ", recall)
        print("F_measure: ", F_measure, ",", " Error: ", error / len(features))
        print()

        trainer.train()