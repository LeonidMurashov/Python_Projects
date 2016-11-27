import json
from copy import deepcopy

lifesFileAdress = './bots/$$$LeonidTheKiller$$$_lifes.m'
dodgeFileAdress = './bots/$$$LeonidTheKiller$$$_dodge.m'
idlingFileAdress = './bots/$$$LeonidTheKiller$$$_idling.m'
LifeMaximum = 100

########################################################
def FindBot(x,y,field):
	bot = [len(field)/2, len(field[0])/2]
	minimal = 9900
	for i in range(len(field)):
		for j in range(len(field[0])):
			if field[i][j] != 0 and (i != x or j != y):
				if minimal > min(abs(x - i), abs(y - j)):
					minimal = min(abs(x - i), abs(y - j))
					bot = [i, j]
	return bot

def GoToPoint(x, y, bX, bY):
	if(x == bX):
		if(y < bY):
			return "fire_down"
		else:
			return "fire_up"
	elif(y == bY):
		if(x > bX):
			return "fire_left"
		else:
			return "fire_right"

	if (abs(bY - y) < abs(bX - x)):
		if (y < bY):
			return "go_down"
		else:
			return "go_up"
	else:
		if (x > bX):
			return "go_left"
		else:
			return "go_right"

def make_choice_Finder(x,y,field):
	bX, bY = FindBot(x, y, field)
	return GoToPoint(x, y, bX, bY)
#######################################################


commands = ["go_right", "go_left", "go_up", "go_down", "fire_right", "fire_left", "fire_up", "fire_down"]
#commands = ["go_up", "go_down", "fire_right", "fire_left"]
height = 0
width = 0
time = 0
fireZones = []
sightZones = []

def IsEmpty(x, y, field):
	if not IsAviable(x, y) or field[x][y] != 0:
		return False
	return True

def IsAviable(x, y):
	if x < 0 or x > width-1 or y < 0 or y > height-1:
		return False
	return True

def GetCommandDirection(command):
	if command[-2:] == "up": return [0, -1]
	if command[-2:] == "wn": return [0, 1]
	if command[-2:] == "ft": return [-1, 0]
	if command[-2:] == "ht": return [1, 0]
	return [0, 0]

def Hit(x, y, field, command):
	direction = GetCommandDirection(command)

	x += direction[0]
	y += direction[1]
	while IsEmpty(x, y, field):
		x += direction[0]
		y += direction[1]
	if IsAviable(x, y):
		field[x][y]['life'] -= 1
		return True, field
	return False, field

def RunCommand(x, y, score, command, field, life):
	move = False
	if command[:2] == "go":
		lastXY = [x, y]
		field[x][y] = 0
		if command == "go_up":
			if IsEmpty(x, y - 1, field): y -= 1
		elif command == "go_down":
			if IsEmpty(x, y + 1, field): y += 1
		elif command == "go_left":
			if IsEmpty(x - 1, y, field): x -= 1
		else:
			if IsEmpty(x + 1, y, field): x += 1
		field[x][y] = {'life' : life}
		if lastXY[0] == x and lastXY[1] == y:
			score -= 2
		else:
			move = True
	else:
		hit, field = Hit(x, y, deepcopy(field), command)
		if hit:
			score += 20

	life -= ((1 + 2*(1 - life/LifeMaximum))*fireZones[x][y] + 0.5*(0 + (life/LifeMaximum))*sightZones[x][y])

	# score -= sightZones[x][y]*1
	# For life bot
	score += 1
	return x, y, score, field, life

def Rec(iteration, x, y, score, field, life, banFire = False):
	if iteration > 2 or life < 1:
		return score, life
	# Do iteration
	maxScore = 0
	maxLife = 0
	leadCommands = []
	for command in commands:
		_x, _y, _score, _field, _life = RunCommand(x, y, score, command, deepcopy(field), life)
		RecScore, RecLife = Rec(iteration + 1, _x, _y, _score, deepcopy(_field), _life, banFire)
		if maxScore < RecScore:
			maxScore = RecScore
		if iteration == 0:
			leadCommands.append([command, RecScore, RecLife])

	if iteration == 0:
		leadCommand = ''
		maxScore = 0
		maxLife = 0
		for command in leadCommands:
			if (banFire and maxLife < command[2] and not command[0][0] == 'f') or maxScore < command[1] and not banFire:
				maxScore = command[1]
				maxLife = command[2]
				leadCommand = command[0]

		return leadCommand
	else:
		return maxScore, life

def BuildFireSightZones(field, x, y):
	# Filling with nils
	fireZones = [[0 for i in range(int(height))] for j in range(int(width))]
	sightZones = [[0 for i in range(int(height))] for j in range(int(width))]
	for i in range(len(field)):
		for j in range(len(field[0])):
			if field[i][j] != 0 and not (i == x and j == y):
				if len(field[i][j]['history']) != 0:
					command = field[i][j]['history'][len(field[i][j]['history']) - 1]

					# Creating fires matrix
					direction = [0, 0]
					if command[0] == 'f':
						direction = GetCommandDirection(command)
					if direction != [0, 0]:
						dx = i + direction[0]
						dy = j + direction[1]
						while IsAviable(dx, dy) and ((dx - direction[0] == i and dy - direction[1] == j) or IsEmpty(dx - direction[0], dy - direction[1], field) or (dx - direction[0] == x and dy - direction[1] == y)):
							fireZones[dx][dy] += 1
							dx += direction[0]
							dy += direction[1]

				# Creating views matrix
				for k in range(i+1, width):
					if not IsAviable(k, j): break
					sightZones[k][j] += 1
					if field[k][j] != 0 and not (k == x and j == y): break
				for k in range(i-1, -1, -1):
					if field[k][j] != 0 and not (k == x and j == y): break
					sightZones[k][j] += 1

				for o in range(j+1, height):
					if not IsAviable(i, o): break
					sightZones[i][o] += 1
					if field[i][o] != 0 and not (i == x and o == y): break
				for o in range(j-1, -1, -1):
					if field[i][o] != 0 and not (i == x and o == y): break
					sightZones[i][o] += 1
				sightZones[i][j] += 2
	return fireZones, sightZones

def CalcMinDistance(x1, y1, x2, y2):
	return min(abs(x1 - x2), abs(y1 - y2))

def IsAnyShootable(x, y, field):
	for i in range(width):
		if field[i][y] != 0 and not (i == x):
			return True
	for j in range(height):
		if field[x][j] != 0 and not (j == y):
			return True
	return False

def ReadAndWriteLife(life):
	lifeList = []
	try:
		lifesFile = open(lifesFileAdress, 'r')
		text = lifesFile.read()
		lifesFile.close()
		lifeList = json.loads(text)
	except:
		a = 5

	# Cleaning file
	if len(lifeList) > 0:
		if lifeList[0] < life:
			lifeList = []

	if len(lifeList) == 5:
		lifeList.pop(0)
	lifeList.append(life)
	text = json.dumps(lifeList)
	lifesFile = open(lifesFileAdress, 'w+')
	lifesFile.write(text)
	lifesFile.close()
	return lifeList

# Looking for dodge coordinates
def ReadDodgeCoordinates():
	dodgeList = []
	try:
		dodgeFile = open(dodgeFileAdress, 'r')
		text = dodgeFile.read()
		dodgeFile.close()
		dodgeList = json.loads(text)
	except:
		a = 5
	return dodgeList

def WriteDodgeCoordinates(dodgeList):
	text = json.dumps(dodgeList)
	dodgeFile = open(dodgeFileAdress, 'w+')
	dodgeFile.write(text)
	dodgeFile.close()

# Looking for dodge coordinates
def ReadIdlingCoordinates():
	idlingList = []
	try:
		idlingFile = open(idlingFileAdress, 'r')
		text = idlingFile.read()
		idlingFile.close()
		idlingList = json.loads(text)
	except:
		a = 5
	return idlingList

def WriteIdlingCoordinates(idlingList):
	text = json.dumps(idlingList)
	idlingFile = open(idlingFileAdress, 'w+')
	idlingFile.write(text)
	idlingFile.close()

def ClearFiles():
	dodgeFile = open(dodgeFileAdress, 'w+')
	dodgeFile.write('')
	dodgeFile.close()

	idlingFile = open(idlingFileAdress, 'w+')
	idlingFile.write('')
	idlingFile.close()

def make_choice(x, y, field):
	global height, width, time, fireZones, sightZones
	# Filling with nils
	height = len(field[0])
	width = len(field)
	life = field[x][y]['life']
	fireZones, sightZones = BuildFireSightZones(field, x, y)
	time = len(field[x][y]['history'])

	if time == 0 or time == 1:
		ClearFiles()

	'''if len(field[x][y]['history']) > 0:
		history = deepcopy(field[x][y]['history'])
		lastMove = history[len(history) - 1]
		history.pop(len(history) - 1)
		sameMovesCount = 1
		if lastMove[0] == 'f':
			while len(history) != 0 and history[len(history) - 1] == lastMove:
				sameMovesCount += 1
				history.pop(len(history) - 1)

		if sameMovesCount > 2:
			banFires = True'''

	# Do iteration of finderBot
	closeCreatures = []
	for i in range(len(field)):
		for j in range(len(field[0])):
			if field[i][j] != 0:
				minDistance = CalcMinDistance(x, y, i, j)
				if (minDistance == 0 and not (i == x and j == y)) or minDistance == 1 or minDistance == 2:
					closeCreatures.append([i, j, field[i][j]])

	idlingList = ReadIdlingCoordinates()
	newField = deepcopy(field)
	for creature in closeCreatures:
		if not IsAnyShootable(creature[0], creature[1], field):
			# Checking for idling on the same place ############## tut oshibka
			similarities = 0
			i = 0
			while i < len(idlingList):
				if time - idlingList[i]['time'] > 10:
					idlingList.pop(i)
					continue
				if idlingList[i]['coordinates'] == [creature[0], creature[1]]:
					similarities += 1
				i += 1

			if similarities < 3:
				# Do finder step
				choice = make_choice_Finder(creature[0], creature[1], field)
				if choice[0] == 'g':
					direction = GetCommandDirection(choice)
					if IsAviable(creature[0] + direction[0],creature[1] + direction[1]):
						newField[creature[0] + direction[0]][creature[1] + direction[1]] = deepcopy(newField[creature[0]][creature[1]])
						newField[creature[0]][creature[1]] = 0
				idlingList.append({'time' : time, 'coordinates' : [creature[0], creature[1]]})
	WriteIdlingCoordinates(idlingList)

	# Ban life trading
	lifeList = ReadAndWriteLife(life)
	banFires = False
	if (lifeList[0] - lifeList[len(lifeList)-1] > 2 or field[x][y]['life'] < 3 and lifeList[0] - lifeList[len(lifeList)-1] > 1) and not len(closeCreatures) == 1:
		banFires = True

	# Dodging single enemy
	if len(closeCreatures) == 1 and IsAnyShootable(x, y, field):
		similarities = 0
		dodgeList = ReadDodgeCoordinates()
		for i in range(len(dodgeList)):
			if time - dodgeList[i]['time'] < 10 and dodgeList[i]['coordinates'] == [closeCreatures[0][0], closeCreatures[0][1]]:
				similarities += 1

		if similarities < 3:
			# Starting dodging
			banFires = True
			dodgeList.append({'time' : time, 'coordinates' : [closeCreatures[0][0], closeCreatures[0][1]]})
			WriteDodgeCoordinates(dodgeList)
			#print("IT DODGES")

	if len(closeCreatures) == 0:
		return make_choice_Finder(x, y, newField)
	return Rec(0, x, y, 0, newField, life, banFires)

if __name__ == "__main__":
	#anLife = {'life' : 4, 'history' : ["fire_up", "fire_right"]}
	#myLife = {'life' : 2, 'history' : ["fire_up", "fire_right", "fire_right", "fire_right"]}
	anLife = {'life': 4, 'history': []}
	myLife = {'life' : 2, 'history' : []}
	field = [[0 for i in range(int(15))] for j in range(int(20))]
	field[5][10] = myLife
	field[2][10] = anLife
	field[5][8] = anLife
	field[9][14] = anLife
	field[2][1] = anLife
	print(make_choice(5, 10, field))
	for j in range(len(field[0])):
		for i in range(len(field)):
			if field[i][j] == 0: print(0, end=' ')
			else: print(field[i][j]['life'], end=' ')

		print('	 ', end='')
		for i in range(len(field)):
			print(fireZones[i][j], end=' ')

		print('	 ', end='')
		for i in range(len(field)):
			print(sightZones[i][j], end=' ')
		print()
	#print(make_choice(1, 2, [ [0, 0, 0, 0, 0], [0, 0, myLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0] ] ))