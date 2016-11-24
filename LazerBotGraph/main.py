from copy import deepcopy

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

def Hit(x, y, field, command):
    direction = []
    if command == "fire_up": direction = [0, -1]
    if command == "fire_down": direction = [0, 1]
    if command == "fire_left": direction = [-1, 0]
    if command == "fire_right": direction = [1, 0]

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
    if command == "go_left" or command == "go_up" or command == "go_down" or command == "go_right":
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
    else:
        hit, field = Hit(x, y, deepcopy(field), command)
        if hit:
            score += 20

    life -= fireZones[x][y]
    score -= sightZones[x][y]*1
    # For life bot
    score += 1
    # TODO life cycle
    return x, y, score, field, life

def Delme(field):
    field[1][1] = 0

def Rec(iteration, x, y, score, field, life):
    if iteration > 4 or life < 1:
        return score
    # Do iteration
    maxScore = 0
    leadCommand = ''
    for command in commands:
        _x, _y, _score, _field, _life = RunCommand(x, y, score, command, deepcopy(field), life)

        '''for i in range(5):
            for j in range(3):
                if field[j][i] == 0:
                    print(0, end=' ')
                else:
                    print(1, end=' ')
            print(end='\n')
        print(end='\n')
        print('x = ', x, 'y = ', y)
        print(end='\n')'''
        RecResult = Rec(iteration + 1, _x, _y, _score, deepcopy(_field), _life)
        if maxScore < RecResult:
            maxScore = RecResult
            if iteration == 0:
                leadCommand = command

    if iteration == 0:
        return leadCommand
    else:
        return maxScore

def BuildFireZones(field, x, y):
    global fireZones, sightZones
    # Filling with nils
    fireZones = [[0 for i in range(int(height))] for j in range(int(width))]
    sightZones = [[0 for i in range(int(height))] for j in range(int(width))]
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] != 0 and not (i == x and j == y):
                if len(field[i][j]['history']) == 0:
                    continue
                command = field[i][j]['history'][len(field[i][j]['history']) - 1]

                # Creating fires matrix
                direction = [0, 0]
                if command == "fire_up": direction = [0, -1]
                if command == "fire_down": direction = [0, 1]
                if command == "fire_left": direction = [-1, 0]
                if command == "fire_right": direction = [1, 0]
                if direction != [0, 0]:
                    dx = i + direction[0]
                    dy = j + direction[1]
                    while IsAviable(dx, dy):
                        fireZones[dx][dy] += 1
                        dx += direction[0]
                        dy += direction[1]

                # Creating views matrix
                for k in range(width):
                    sightZones[k][j] += 1
                for o in range(height):
                    sightZones[i][o] += 1


def make_choice(x, y, field):
    global height, width, time
    # Filling with nils
    height = len(field[0])
    width = len(field)
    life = field[x][y]['life']
    #time = len(field[x][y]['history'])

    #return "go_right"
    BuildFireZones(field, x, y)
    return Rec(0, x, y, 0, field, life)

if __name__ == "__main__":
    anLife = {'life' : 1, 'history' : ["fire_up", "fire_right"]}
    myLife = {'life' : 10, 'history' : ["fire_up", "fire_right"]}
    field = [[0 for i in range(int(20))] for j in range(int(15))]
    field[5][15] = myLife
    field[7][11] = anLife
    field[5][13] = anLife
    field[9][19] = anLife
    field[2][3] = anLife
    print(make_choice(5, 15, field))
    #print(make_choice(1, 2, [ [0, 0, 0, 0, 0], [0, 0, myLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0] ] ))