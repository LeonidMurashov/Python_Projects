import json

from pybrain import SigmoidLayer
from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
width = 0
height = 0
InputLayerSize = 4
commands = ["go_right", "go_left", "go_up", "go_down", "fire_right", "fire_left", "fire_up", "fire_down"]

def FormatData(x, y, field):
	data = []
	for i in range(width):
		for j in range(height):
			if field[i][j] != 0 and not (i == x and j == y):
				data.append([field[x][y]['life'], abs(i - x), abs(j - y), field[i][j]['life']])
	return data

if __name__ == "__main__":
	global width, height, commands
	f = open('/media/sf_Python/PyCharm/LazerBotGraph_dataSet/features.json', 'r')
	text = f.read()
	f.close()

	features = []
	rawFeatures = json.loads(text)
	width = len(rawFeatures[0]['field'])
	height = len(rawFeatures[0]['field'][0])

	for rawFeature in rawFeatures:
		player = rawFeature['player']
		field = rawFeature['field']
		decisionRaw = rawFeature['decision']

		fieldData = FormatData(player[0], player[1], field)
		num = 0

		for playerData in fieldData:
			isTrue = 0
			if player[0] < playerData[1] and decisionRaw[-4:] == 'left' or player[0] > playerData[1] and decisionRaw[-4:] == 'ight' or player[1] < playerData[2] and decisionRaw[-4:] == 'down' or player[1] > playerData[2] and decisionRaw[-2:] == 'up':
				isTrue = 1
			features.append([playerData, isTrue])

	dataSet = SupervisedDataSet(InputLayerSize, 1)
	for feature in features:
		dataSet.addSample(feature[0], feature[1])

	Network = buildNetwork(dataSet.indim, InputLayerSize * 2, InputLayerSize * 2, 1, hiddenclass=SigmoidLayer, outclass=SigmoidLayer, bias=True)
	trainer = BackpropTrainer(Network, dataSet, learningrate=0.001, momentum=0.001)

	trainer.trainUntilConvergence()


	rightAnswers = 0
	for feature in features:
		outputs = Network.activate(feature[0])

		maxValue = -1
		maxValueIndex = -1
		if outputs[0] > 0.5 and feature[1] == 1:
			rightAnswers += 1

		print(outputs[0], feature[1], outputs[0] > 0.5 and feature[1] == 1)

	print('Right answers: ', rightAnswers / len(features) * 100, "%")
	Network._name = 'SupervisedNetwork'
	NetworkWriter.writeToFile(Network, "BestSupervised")