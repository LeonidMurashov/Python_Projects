import os
import random
import time

import _thread
from dask.tests.test_base import np
from pybrain import SigmoidLayer, FeedForwardNetwork
from pybrain.tools.shortcuts import buildNetwork
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader

version = 15
graphFileAdress = '/media/sf_Python/PyCharm/LazerBotNeural/Graph' + str(version) + '.csv'
averageFileAdress = '/media/sf_Python/PyCharm/LazerBotNeural/GraphAverage' + str(version) + '.csv'
bestBotFileAdress = 'BestLazerBot' + str(version) + '.xml'
matrix = []
width = 20
height = 12
creaturesPlaying = []
creatures = []
shoots = []
moves = ["go_up", "go_down", "go_right", "go_left", "fire_up", "fire_down", "fire_left", "fire_right"]
scoreRecord = 0
Population_Size =100 # Must be dividable by 10
Plays_Count = 3
InputLayerSize = 6*(width + height - 4) + 9

def IsEmpty(x, y):
	if not IsAviable(x, y):
		return False
	for creature in creaturesPlaying:
		if creature.x == x and creature.y == y:
			return False
	return True

def IsAviable(x, y):
	if x < 0 or x > width-1 or y < 0 or y > height-1:
		return False
	return True


def AnalizeCeil(x, y, field):
	if IsAviable(x, y):
		if field[x][y] == '|' or field[x][y] == '--':
			return 0
		else:
			return field[x][y]
	else:
		return -10

def FormatData(x, y, field):
	data = []
	# Middle
	for i in range(3):
		for j in range(3):
			cX = i - 1 + x
			cY = j - 1 + y
			data.append(AnalizeCeil(cX, cY, field))
	# Up
	for i in range(3):
		for j in range(height - 2):
			cX = i - 1 + x
			cY = - j - 2 + y
			data.append(AnalizeCeil(cX, cY, field))
	# Down
	for i in range(3):
		for j in range(height - 2):
			cX = i - 1 + x
			cY = j + 2 + y
			data.append(AnalizeCeil(cX, cY, field))
	# Left
	for i in range(width - 2):
		for j in range(3):
			cX = - i - 2 + x
			cY = j - 1 + y
			data.append(AnalizeCeil(cX, cY, field))
	# Right
	for i in range(width - 2):
		for j in range(3):
			cX = i + 2 + x
			cY = j - 1 + y
			data.append(AnalizeCeil(cX, cY, field))
	return data
	

class Creature:
	x = y = -1
	life = 10
	score = 0
	direction = []
	shootingMove = False
	Network = 0
	passingProbability = 0

	def __init__(self, Network=0):
		if Network == 0:
			self.Network = buildNetwork(int(InputLayerSize), int(InputLayerSize / 2), 8, hiddenclass=SigmoidLayer, outclass=SigmoidLayer, bias=True)
		else:
			self.Network = Network

	def SetXY(self, x, y):
		self.x = x
		self.y = y

	def GetNetworkParams(self):
		return self.Network.params

	def make_choice(self, x, y, field):
		data = FormatData(x, y, field)

		outputs = self.Network.activate(data)
		maxValue = -1
		maxValueIndex = -1
		for i in range(len(outputs)):
			if outputs[i] > maxValue:
				maxValue = outputs[i]
				maxValueIndex = i
		return moves[maxValueIndex]


	def AskChoice(self):
		if self.life < 1:
			return

		choice = self.make_choice(self.x, self.y, matrix)
		if choice == "go_up" or choice == "go_down" or choice == "go_left" or choice == "go_right":
			self.shootingMove = False
		else:
			self.shootingMove = True

		if choice == "go_up" or choice == "fire_up":
			self.direction = [0, -1]
		if choice == "go_down" or choice == "fire_down":
			self.direction = [0, 1]
		if choice == "go_left" or choice == "fire_left":
			self.direction = [-1, 0]
		if choice == "go_right" or choice == "fire_right":
			self.direction = [1, 0]

	def Run(self):
		if self.life < 1:
			self.x = -1
			self.y = -1
			return
		self.score += 1

		if self.shootingMove:
			currX = self.x + self.direction[0]
			currY = self.y + self.direction[1]
			while IsEmpty(currX, currY):
				currX += self.direction[0]
				currY += self.direction[1]

			if IsAviable(currX, currY):
				for creature in creaturesPlaying:
					if creature.x == currX and creature.y == currY:
						creature.life -= 1
						self.score += 20
						break
			if IsAviable(self.x + self.direction[0], self.y  + self.direction[1]):
				shoots.append([[max(self.x, self.x + self.direction[0]), max(self.y, self.y + self.direction[1])], [max(currX, currX - self.direction[0]), max(currY, currY - self.direction[1])]])

		else:
			if IsEmpty(self.x + self.direction[0], self.y + self.direction[1]):
				self.x += self.direction[0]
				self.y += self.direction[1]

def DrawMatrix():
	DrawShoots()
	for creature in creaturesPlaying:
		if IsAviable(creature.x,creature.y):
			matrix[creature.x][creature.y] = creature.life

def CreaturesMovesComparator(a):
	if not a.shootingMove: #like moving is less than shooting
		return 0
	return 1

def CreaturesScoresComparator(a):
	return a.score

def DrawShoots():
	for shoot in shoots:
		if shoot[0] == shoot[1]:
			continue
		if shoot[0][0] == shoot[1][0]:
			for y in range(abs(shoot[0][1] - shoot[1][1])):
				matrix[shoot[0][0]][y + min(shoot[0][1], shoot[1][1])] = '|' # Vertical slash
		else:
			for x in range(abs(shoot[0][0] - shoot[1][0])):
				matrix[x + min(shoot[0][0], shoot[1][0])][shoot[0][1]] = "--" # Horizontal slash
	shoots.clear()

def Run():
	for creature in creaturesPlaying:
		creature.AskChoice()

	random.shuffle(creaturesPlaying)
	creaturesPlaying.sort(key=CreaturesMovesComparator)

	for creature in creaturesPlaying:
		creature.Run()

def Play(printing = True):
	global matrix

	# Reheal all
	for creature in creaturesPlaying:
		creature.life = 10

	# Filling with nils
	matrix = [[0 for i in range(int(height))] for j in range(int(width))]
	DrawMatrix()

	# Game cycle
	iteration = 0
	while True:
		Run()
		# Filling with nils
		matrix = [[0 for i in range(int(height))] for j in range(int(width))]
		DrawMatrix()
		if printing:
			for i in range(height):
				for j in range(width):
					if matrix[j][i] == "--":  # print("\33[41m", matrix[j][i], "\33[0m",  ' ',end='')
						print(matrix[j][i], end='')  # print( matrix[j][i], end=' ')
					elif matrix[j][i] == '|' or matrix[j][i] < 10:
						print(matrix[j][i], end=' ')
					else:
						print(matrix[j][i], end='')
				print(end='\n')
			print(end='\n')

		# time.sleep(0.5)
		iteration += 1
		if iteration == 30:
			break

# Merge and mutate two numbers
def Merge(a, b, mutations):
	k = 1
	sign = 1
	if random.random() < mutations:
		k = random.random()*1.5 + 0.5
		if random.random() < 0.05:
			sign = -1

	return ((a + b)/2)*k*sign

# Breed two creatures
def Breed(creatureA, creatureB):
	finalNetwork = buildNetwork(int(InputLayerSize), int(InputLayerSize / 2), 8, hiddenclass=SigmoidLayer, outclass=SigmoidLayer, bias=True)

	paramsA = creatureA.GetNetworkParams()
	paramsB = creatureB.GetNetworkParams()
	finalParams = []

	mutations = 0
	if random.random() < 0.5:
		mutations = 1
	# Merging weights and biases
	for i in range(len(paramsA)):
		finalParams.append(Merge(paramsA[i], paramsB[i], mutations))

	finalNetwork._setParameters(finalParams)
	return Creature(finalNetwork)

def ShuffleCreaturesPlaying():
	for creature in creaturesPlaying:
		x = random.randint(0, width - 1)
		y = random.randint(0, height - 1)
		while not IsEmpty(x, y):
			x = random.randint(0, width - 1)
			y = random.randint(0, height - 1)
		creature.SetXY(x, y)

def grapherThread():
	os.system("/home/leonid/anaconda3/bin/python /media/sf_Python/PyCharm/Plotter/mainPlotter.py " + graphFileAdress + " " + averageFileAdress)

if __name__ == "__main__":

	# Creating first generation
	for i in range(Population_Size):
		creatures.append(Creature())

	iteration = 0
	while True:
		print("---------------------------------")
		print("----------NEW ITERATION----------")
		print("-----------number: ", iteration,"-------------")
		print("---------------------------------")

		time.sleep(1)

		# Run creatures
		playIteration = 0
		while playIteration != Population_Size:
			creaturesPlaying = creatures[0 + playIteration:10 + playIteration]
			playIteration += 10
			for i in range(Plays_Count):
				ShuffleCreaturesPlaying()
				Play(True)

		# Getting average score and some data for averageFile
		allScore = 0
		for creature in creatures:
			creature.score /= Plays_Count
			allScore += creature.score
		allScore /= len(creatures)
		creatures.sort(key=CreaturesScoresComparator, reverse=True)

		# Finding the best and save it in case of beating record
		bestCreature = creatures[0]
		print("Best score:", bestCreature.score)
		graphFile = open(graphFileAdress, 'a')
		graphFile.write(str(iteration))
		graphFile.write(';')
		graphFile.write(str(bestCreature.score))
		graphFile.write('\n')
		graphFile.close()
		if scoreRecord < bestCreature.score:
			scoreRecord = bestCreature.score
			NetworkWriter.writeToFile(bestCreature.Network, bestBotFileAdress)

		# Graphing average
		print("Average score:", allScore)
		graphFile = open(averageFileAdress, 'a')
		graphFile.write(str(iteration))
		graphFile.write(';')
		graphFile.write(str(allScore))
		graphFile.write('\n')
		graphFile.close()

		# Opening graph program
		if iteration == 0: _thread.start_new_thread(grapherThread,())

		# Getting half-final
		halfFinal = []
		random.shuffle(creatures)
		scoresSum = 0
		for creature in creatures: scoresSum += creature.score
		for creature in creatures: creature.passProbability = creature.score / scoresSum
		# Adding relying on probability
		i = 0
		isPassed = [False for i in range(Population_Size)]
		while len(halfFinal) != Population_Size / 2:
			if not creatures[i%Population_Size].passProbability > random.random() and isPassed[i%Population_Size] == False:
				halfFinal.append(creatures[i%Population_Size])
				isPassed[i%Population_Size] = True
			i = random.randint(0, Population_Size)

		# Breeding new generation
		newGeneration = []
		while len(newGeneration) != Population_Size:
			newGeneration.append(Breed(random.choice(halfFinal), random.choice(halfFinal)))

		# Replace old generation to young
		del creatures
		creatures = newGeneration
		iteration += 1

'''bestCreature.x = random.randint(0, width - 1)
bestCreature.y = random.randint(0, height - 1)
bestCreature.score = 0
bestCreature.life = 10'''