from sklearn import svm
import numpy as np
features = []
features_for_test = []
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
    ReadFeatures()
    print("All features read.\n ")

    #leaving some data for testing
    features_for_test = features[:1500]
    del features[:1500]

    clf = svm.SVC()

    X = np.array([features[:len(features[0])-2]])
    Y = np.array([features[len(features[0])-1]])
    for feature in features:
        np.append(X, feature[:len(feature)-2])
        np.append(Y, feature[len(feature)-1])

    for i in range(500):
        clf.fit(X, Y)

        TP = TN = FP = FN = 0
        error = 0
        for feature in features_for_test:
            output = clf.predict(feature[:len(feature)-2])

            answer = output[0] > 0.5
            rightAnswer = feature[len(feature) - 1]
            error += rightAnswer - output[0]
            if answer:
                if rightAnswer:
                    TP += 1
                else:
                    FP += 1
            else:
                if rightAnswer:
                    FN += 1
                else:
                    TN += 1

        recall = (TP / (TP + FN)) if ((TP + FN) != 0) else 0
        precision = (TP / (TP + FP)) if ((TP + FP) != 0) else 0
        F_measure = 2 * ((precision * recall) / (precision + recall)) if (precision + recall != 0) else 0
        print("TP: ", TP, ", TN: ", TN, ", FP: ", FP, ", FN: ", FN)
        print("Precision: ", precision, ",", " Recall: ", recall)
        print("F_measure: ", F_measure, ",", " Error: ", error / len(features_for_test))
        print()

        if F_measureRecord < F_measure:
            F_measureRecord = F_measure
            file = open(outputFileAdress, 'w')
            file.write("id,passed\n")
            for feature in features_test:
                output = clf.predict(feature[:len(feature)-2])
                answer = output[0] > 0.5
                file.write(str(int(feature[0])) + "," + str(int(answer)) + '\n')
            file.close()