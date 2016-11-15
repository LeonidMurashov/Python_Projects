from pybrain import TanhLayer, SoftmaxLayer
from pybrain.structure.modules.sigmoidlayer import SigmoidLayer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import random

features = []
features_for_test = []
featuresRandom = []
features_test = []
featuresFileAdress = '/media/sf_Python/PyCharm/GotoNeural/features.csv'
features_testFileAdress = '/media/sf_Python/PyCharm/GotoNeural/features_test.csv'
outputFileAdress = '/media/sf_Python/PyCharm/GotoNeural/Network_Precision.csv'
F_measureRecord = 0

# Reading training data
def ReadFeatures():
    print("Reading features...\n ")
    prefeatures = []

    # Reading training features
    file = open(featuresFileAdress, 'r')
    for str in file:
        prefeatures.append(str.split(','))
    del(prefeatures[0])

    for prefeature in prefeatures:
        unitsDouble = []
        for sub in prefeature:
            unitsDouble.append(float(sub))
        del(unitsDouble[0])
        features.append(unitsDouble)
    file.close()
    prefeatures.clear()

    # Reading test features
    file = open(features_testFileAdress, 'r')
    for str in file:
        prefeatures.append(str.split(','))
    del(prefeatures[0])

    for prefeature in prefeatures:
        unitsDouble = []
        for sub in prefeature:
            unitsDouble.append(float(sub))
        features_test.append(unitsDouble)
    file.close()
    del prefeatures

if __name__ == "__main__":
    random.seed();
    ReadFeatures()
    print("All features read.\n ")

    # Leaving 50/50 positives/negatives
    positives = negatives = 0
    for feature in features:
        if feature[len(feature)-1] == 0:
            negatives+=1
        else:
            positives+=1
    myi = 0
    while positives / negatives < 0.59:
        if features[myi][len(features[myi])-1] == 0:
            del(features[myi])
            negatives-=1
        else:
            myi+=1

        # Random mix
    '''featuresSize = len(features)
    for i in range(featuresSize):
        featuresRandom.append([])
    myi = 0
    while len(features) != 0:
        rand = int(random.random()*10000%featuresSize)
        if featuresRandom[rand] == []:
            featuresRandom[rand] = features[myi]
            del features[myi]
    features = featuresRandom'''

    features_for_test = features[:200]
    del features[:200]

    dataSet = SupervisedDataSet(len(features[0]) - 2, 1)
    for feature in features:
        dataSet.addSample(feature[:len(feature) - 2], feature[len(feature) - 1])

    Network = buildNetwork(dataSet.indim, 6, 1, hiddenclass=SigmoidLayer, outclass=SigmoidLayer)
    trainer = BackpropTrainer(Network, dataSet);#, learningrate=0.00005, momentum=0.00005)

    while True:
        TP = TN = FP = FN = 0
        error = 0
        for feature in features_for_test:
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
        print("F_measure: ", F_measure, ",", " Error: ", error / len(features_for_test))
        print()

        if F_measureRecord < F_measure:
            F_measureRecord = F_measure
            file = open(outputFileAdress, 'w')
            file.write("id,passed\n")
            for feature in features_test:
                output = Network.activate(feature[1:dataSet.indim + 1])
                answer = output[0] > 0.5
                file.write(str(int(feature[0])) + "," + str(int(answer)) + '\n')
            file.close()

        trainer.train()