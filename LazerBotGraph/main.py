commands = ["go_right", "go_left", "go_up", "go_down", "fire_right", "fire_left", "fire_up", "fire_down"]
height = 0
width = 0
time = 0

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
        hit, field = Hit(x, y, field, command)
        if hit:
            score += 20

    # For life bot
    score += 1
    # TODO life cycle
    return x, y, score, field, life

def Rec(iteration, x, y, score, field, life):
    if iteration > 2:
        return score
    # Do iteration
    maxScore = 0
    leadCommand = ''
    for command in commands:
        _x, _y, _score, _field, _life = RunCommand(x, y, score, command, field, life)
        RecResult = Rec(iteration + 1, _x, _y, _score, _field, _life)
        if maxScore < RecResult:
            maxScore = RecResult
            if iteration == 0:
                leadCommand = command

    if iteration == 0:
        return leadCommand
    else:
        return maxScore

def make_choice(x, y, field):
    global height, width, time
    # Filling with nils
    height = len(field)
    width = len(field[0])
    life = field[x][y]['life']
    #time = len(field[x][y]['history'])

    return Rec(0, x, y, 0, field, life)

if __name__ == "__main__":
    anLife = {'life' : 1}
    myLife = {'life' : 10}
    print(make_choice(1, 1, [ [0, 0, 0], [0, myLife, 0], [anLife, 0, 0] ]))