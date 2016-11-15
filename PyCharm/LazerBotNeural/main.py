import random
import time

matrix = []
width = 20
height = 12
creatures = []
shoots = []

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

class Creature:
    x = y = 0
    life = 10
    direction = []
    shootingMove = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def make_choice(self, x, y, field):
        return random.choice(["fire_up", "fire_right"])
        #return random.choice(["go_down", "go_up", "go_left", "go_right", "fire_up", "fire_down", "fire_left","fire_right"])

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
                        break
            if IsAviable(self.x + self.direction[0], self.y  + self.direction[1]):
                shoots.append([[currX, currY - self.direction[1]], [self.x + self.direction[0], self.y]])

        else:
            if IsEmpty(self.x + self.direction[0], self.y + self.direction[1]):
                self.x += self.direction[0]
                self.y += self.direction[1]

def NilMatrix():
    # Filling with nils
    '''for i in range(width):
    a = []
    for j in range(height):
        a.append(0)
    matrix.append(a)'''

def DrawMatrix():
    #NilMatrix()
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

    DrawShoots()

if __name__ == "__main__":
    for i in range(5):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        while not IsEmpty(x, y):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
        creatures.append(Creature(x, y))

    # Game cycle
    while True:
        # Filling with nils
        matrix = [[0 for i in range(int(height))] for j in range(int(width))]
        DrawMatrix()
        Run()
        for i in range(height):
            for j in range(width):
                if(matrix[j][i] == '-' or matrix[j][i] == '|' or matrix[j][i] < 10):
                    print(matrix[j][i], end=' ')
                else:
                    print(matrix[j][i], end='')
            print(end='\n')
        print(end='\n')
        time.sleep(1)
