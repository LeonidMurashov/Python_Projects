import copy
import random
import time

from dask.tests.test_base import np
from pybrain import SigmoidLayer, FeedForwardNetwork
from pybrain.tools.shortcuts import buildNetwork
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader

import FinderBot

networkFileAdress = '/media/sf_Python/PyCharm/LaserBotSupervised/BestSupervised'

matrix = []
width = 20
height = 12
creaturesPlaying = []
creatures = []
shoots = []
commands = ["go_right", "go_left", "go_up", "go_down", "fire_right", "fire_left", "fire_up", "fire_down"]
scoreRecord = 0
Population_Size = 1500  # Must be dividable by 10
InputLayerSize = 45
networkName = ''

def IsEmpty(x, y):
	if not IsAviable(x, y):
		return False
	for creature in creaturesPlaying:
		if creature.x == x and creature.y == y:
			return False
	return True

def IsAviable(x, y):
	if x < 0 or x > width - 1 or y < 0 or y > height - 1:
		return False
	return True

def FormatData(x, y, field):

	data = [x, y, field[x][y]]
	for i in range(width):
		for j in range(height):
			if field[i][j] != 0 and not (i == x and j==y):
				data.append(i - x)
				data.append(j - y)
				data.append(field[i][j])

	while len(data) != InputLayerSize:
		data.append(0)
		data.append(-1)
		data.append(-1)
	return data

class Creature:
	x = y = -1
	life = 10
	score = 0
	direction = []
	shootingMove = False
	Network = 0
	passingProbability = 0
	decision = ''

	def __init__(self, Network=0):
		if Network == 0:
			self.Network = buildNetwork(int(InputLayerSize), int(InputLayerSize), 8, hiddenclass=SigmoidLayer,
										outclass=SigmoidLayer, bias=True)
		else:
			self.Network = Network

	def SetXY(self, x, y):
		self.x = x
		self.y = y

	def GetNetworkParams(self):
		return self.Network.params

	def make_choice(self, x, y, field):

		if self.Network._name == 'SupervisedNetwork':
			data = FormatData(x, y, field)

			outputs = self.Network.activate(data)
			maxValue = -1
			maxValueIndex = -1
			for i in range(len(outputs)):
				if outputs[i] > maxValue:
					maxValue = outputs[i]
					maxValueIndex = i
			return commands[maxValueIndex]
		else:
			return FinderBot.make_choice(x, y, field)


	def AskChoice(self):
		if self.life < 1:
			return

		_field = copy.deepcopy(matrix)

		# Pre-format
		for i in range(width):
			for j in range(height):
				if _field[i][j] == '|' or _field[i][j] == '--':
					_field[i][j] = 0

		choice = self.make_choice(self.x, self.y, _field)
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
			if IsAviable(self.x + self.direction[0], self.y + self.direction[1]):
				shoots.append([[max(self.x, self.x + self.direction[0]), max(self.y, self.y + self.direction[1])],
							   [max(currX, currX - self.direction[0]), max(currY, currY - self.direction[1])]])

		else:
			if IsEmpty(self.x + self.direction[0], self.y + self.direction[1]):
				self.x += self.direction[0]
				self.y += self.direction[1]

def DrawMatrix():
	DrawShoots()
	for creature in creaturesPlaying:
		if IsAviable(creature.x, creature.y):
			matrix[creature.x][creature.y] = creature.life

def CreaturescommandsComparator(a):
	if not a.shootingMove:  # like moving is less than shooting
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
				matrix[shoot[0][0]][y + min(shoot[0][1], shoot[1][1])] = '|'  # Vertical slash
		else:
			for x in range(abs(shoot[0][0] - shoot[1][0])):
				matrix[x + min(shoot[0][0], shoot[1][0])][shoot[0][1]] = "--"  # Horizontal slash
	shoots.clear()

def Run():
	for creature in creaturesPlaying:
		creature.AskChoice()

	#random.shuffle(creaturesPlaying)
	creaturesPlaying.sort(key=CreaturescommandsComparator)

	for creature in creaturesPlaying:
		creature.Run()

def Play(printing=True):
	global matrix
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
					needContinue = 0
					for creature in creatures:
						if creature.Network.name == networkName:
							if i == creature.y and j == creature.x:
								print('*', end=' ')
								needContinue = 1
					if needContinue:
						continue

					if matrix[j][i] == "--":  # print("\33[41m", matrix[j][i], "\33[0m",  ' ',end='')
						print(matrix[j][i], end='')  # print( matrix[j][i], end=' ')
					elif matrix[j][i] == '|' or matrix[j][i] < 10:
						print(matrix[j][i], end=' ')
					else:
						print(matrix[j][i], end='')
				print(end='\n')
			print(end='\n')

		time.sleep(0.3)
		iteration += 1
		if iteration == 30:
			print("--------iteration ended----------")
			break

def ShuffleCreaturesPlaying():
	for creature in creaturesPlaying:
		x = random.randint(0, width - 1)
		y = random.randint(0, height - 1)
		while not IsEmpty(x, y):
			x = random.randint(0, width - 1)
			y = random.randint(0, height - 1)
		creature.SetXY(x, y)

if __name__ == "__main__":

	iteration = 0
	while True:

		creatures.clear()
		# Creating generation
		for i in range(10):
			creatures.append(Creature())
		creatures[0].Network = NetworkReader.readFrom(networkFileAdress)
		networkName = creatures[0].Network.name

		print("---------------------------------")
		print("----------NEW ITERATION----------")
		print("-----------number: ", iteration, "-------------")
		print("---------------------------------")
		time.sleep(1)

		for creature in creatures:
			creature.life = 10

		# Run creatures
		creaturesPlaying = creatures
		ShuffleCreaturesPlaying()
		Play(True)

		# Finding the best
		'''bestScore = 0
		for creature in creatures:
			if bestScore < creature.score:
				bestScore = creature.score'''
		creatures.sort(key=CreaturesScoresComparator, reverse=True)
		print("Best score:", creatures[0].score)
		for creature in creatures:
			if creature.Network.name == networkName:
				print("NN score: ", creature.score, " Name: ", creature.Network.name)
				break
'''bestCreature.x = random.randint(0, width - 1)
bestCreature.y = random.randint(0, height - 1)
bestCreature.score = 0
bestCreature.life = 10'''