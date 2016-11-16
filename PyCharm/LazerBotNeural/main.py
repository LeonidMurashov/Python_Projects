import random
import time
from pybrain import supervised, SigmoidLayer
from pybrain.tools.shortcuts import buildNetwork

matrix = []
width = 20
height = 12
creatures = []
shoots = []
moves = ["go_up", "go_down", "go_right", "go_left", "fire_up", "fire_down", "fire_left", "fire_right"]

def IsEmpty(x, y):
    if not IsAviable(x, y):
        return False
    for creature in creatures:
        if creature.x == x and creature.y == y:
            return False
    return True

def IsAviable(x, y):
    if x < 0 or x > width-1 or y < 0 or y > height-1:
        return False
    return True


def AnalizeCeil(x, y, field):
    if IsAviable(x, y):
        if field[x][y] == '|' or field[x][y] == '-':
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
    x = y = 0
    life = 10
    score = 0
    direction = []
    shootingMove = False
    Network = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Network = buildNetwork(6*(width + height - 4) + 9, 90, 8, hiddenclass=SigmoidLayer, outclass=SigmoidLayer, bias=True)

    def make_choice(self, x, y, field):
        a = FormatData(x, y, field)
        outputs = self.Network.activate(a)
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
                for creature in creatures:
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
    for creature in creatures:
        if IsAviable(creature.x,creature.y):
            matrix[creature.x][creature.y] = creature.life

def CreaturesComparator(a):
    if not a.shootingMove: #like moving is less than shooting
        return 0
    return 1

def DrawShoots():
    for shoot in shoots:
        if shoot[0] == shoot[1]:
            continue
        if shoot[0][0] == shoot[1][0]:
            for y in range(abs(shoot[0][1] - shoot[1][1])):
                matrix[shoot[0][0]][y + min(shoot[0][1], shoot[1][1])] = '|' # Vertical slash
        else:
            for x in range(abs(shoot[0][0] - shoot[1][0])):
                matrix[x + min(shoot[0][0], shoot[1][0])][shoot[0][1]] = '-' # Horizontal slash
    shoots.clear()

def Run():
    for creature in creatures:
        creature.AskChoice()

    random.shuffle(creatures)
    creatures.sort(key=CreaturesComparator)

    for creature in creatures:
        creature.Run()

if __name__ == "__main__":
    while True:
        for i in range(11):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            while not IsEmpty(x, y):
                x = random.randint(0, width-1)
                y = random.randint(0, height-1)
            creatures.append(Creature(x, y))

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
            for i in range(height):
                for j in range(width):
                    if matrix[j][i] == '-' or matrix[j][i] == '|':#print("\33[41m", matrix[j][i], "\33[0m",  ' ',end='')
                        print(matrix[j][i], end=' ')#print( matrix[j][i], end=' ')
                    elif matrix[j][i] < 10:
                        print(matrix[j][i], end=' ')
                    else:
                        print(matrix[j][i], end='')
                print(end='\n')
            print(end='\n')

            time.sleep(0.5)
            iteration += 1
            if iteration == 100:
                break
        print("---------------------------------")
        print("----------NEW ITERATION----------")
        print("---------------------------------")

        # Finding the best
        bestCreature = 0
        maxScore = -1
        for creature in creatures:
            if creature.score > maxScore:
                maxScore = creature.score
                bestCreature = creature

        bestCreature.x = random.randint(0, width - 1)
        bestCreature.y = random.randint(0, height - 1)

        time.sleep(1)
        creatures.clear()
        creatures.append(bestCreature)