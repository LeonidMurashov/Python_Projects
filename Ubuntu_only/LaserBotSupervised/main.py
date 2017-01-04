import json

from pybrain import SigmoidLayer
from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
width = 0
height = 0
InputLayerSize = 45
commands = ["go_right", "go_left", "go_up", "go_down", "fire_right", "fire_left", "fire_up", "fire_down"]

def FormatData(x, y, field):
	data = [x, y, field[x][y]['life']]
	for i in range(width):
		for j in range(height):
			if field[i][j] != 0 and not (i == x and j==y):
				data.append(i - x)
				data.append(j - y)
				data.append(field[i][j]['life'])

	while len(data) != InputLayerSize:
		data.append(0)
		data.append(-1)
		data.append(-1)
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
		for num in range(len(commands)):
			if decisionRaw == commands[num]:
				break
		decision = [0, 0, 0, 0, 0, 0, 0, 0]
		decision[num] = 1

		features.append([fieldData, decision])

	dataSet = SupervisedDataSet(InputLayerSize, 8)
	for feature in features:
		dataSet.addSample(feature[0], feature[1])

	Network = buildNetwork(dataSet.indim, InputLayerSize*2, InputLayerSize*2, 8, hiddenclass=SigmoidLayer, outclass=SigmoidLayer, bias=True)
	trainer = BackpropTrainer(Network, dataSet, learningrate=0.001, momentum=0.001)
	trainer.trainUntilConvergence()
	#trainer.trainEpochs(10000)
	
	rightAnswers = 0
	for feature in features:
		outputs = Network.activate(feature[0])

		maxValue = -1
		maxValueIndex = -1
		for i in range(len(outputs)):
			if outputs[i] > maxValue:
				maxValue = outputs[i]
				maxValueIndex = i
		if feature[1][maxValueIndex] == 1:
			rightAnswers += 1

		printOutputs = [int(output*10)/10 for output in outputs]
		print(printOutputs, feature[1], feature[1][maxValueIndex] == 1)

	print('Right answers: ', rightAnswers/len(features) * 100, "%")
	Network._name = 'SupervisedNetwork'
	NetworkWriter.writeToFile(Network, "BestSupervised")