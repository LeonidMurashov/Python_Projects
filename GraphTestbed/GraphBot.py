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

    life -= (1 + 2*(1 - life/10))*fireZones[x][y] + 0.5*(0 + (life/10))*sightZones[x][y]

    #score -= sightZones[x][y]*1
    # For life bot
    score += 1
    return x, y, score, field, life

def Rec(iteration, x, y, score, field, life, banFire = False):
    if iteration > 2 or life < 1:
        return score
    # Do iteration
    maxScore = 0
    leadCommands = []
    for command in commands:
        _x, _y, _score, _field, _life = RunCommand(x, y, score, command, deepcopy(field), life)
        RecResult = Rec(iteration + 1, _x, _y, _score, deepcopy(_field), _life)
        if maxScore < RecResult:
            maxScore = RecResult
        if iteration == 0:
            leadCommands.append([command, RecResult])

    if iteration == 0:
        leadCommand = ''
        maxScore = 0
        for command in leadCommands:
            if maxScore < command[1] and not(banFire and command[0][0] == 'f'):
                maxScore = command[1]
                leadCommand = command[0]
        return leadCommand
    else:
        return maxScore

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
                    if command == "fire_up": direction = [0, -1]
                    if command == "fire_down": direction = [0, 1]
                    if command == "fire_left": direction = [-1, 0]
                    if command == "fire_right": direction = [1, 0]
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

def make_choice(x, y, field):
    global height, width, time, fireZones, sightZones
    # Filling with nils
    height = len(field[0])
    width = len(field)
    life = field[x][y]['life']
    #time = len(field[x][y]['history'])

    #return "go_right"
    fireZones, sightZones = BuildFireSightZones(field, x, y)

    # Ban life trading
    banFires = False
    if len(field[x][y]['history']) > 0:
        history = deepcopy(field[x][y]['history'])
        lastMove = history[len(history) - 1]
        history.pop(len(history) - 1)
        sameMovesCount = 1
        if lastMove[0] == 'f':
            while len(history) != 0 and history[len(history) - 1] == lastMove:
                sameMovesCount += 1
                history.pop(len(history) - 1)

        if sameMovesCount > 2 and field[x][y]['life'] < 8:
            banFires = True

    # TODO: if there are no bots in line, do iteration of finderBot

    return Rec(0, x, y, 0, field, life, banFires)

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

        print('     ', end='')
        for i in range(len(field)):
            print(fireZones[i][j], end=' ')

        print('     ', end='')
        for i in range(len(field)):
            print(sightZones[i][j], end=' ')
        print()
    a = 5
    #print(make_choice(1, 2, [ [0, 0, 0, 0, 0], [0, 0, myLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0], [0, 0, anLife, 0, 0] ] ))