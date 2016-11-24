fireAtMe = []
width = 0
height = 0

def IsEmpty(x, y, field):
    if not IsAviable(x, y) or field[x][y] != 0:
        return False
    return True

def IsAviable(x, y):
    if x < 0 or x > width-1 or y < 0 or y > height-1:
        return False
    return True

def GetAimAndDirection(str):
    aim = 0 # Going, not firing
    if str[:1] != "go":
        aim = 1
    if str == "fire_up" or str == "go_up": return aim, [0, -1]
    if str == "fire_down" or str == "go_down": return aim, [0, 1]
    if str == "fire_left" or str == "go_left": return aim, [-1, 0]
    if str == "fire_right" or str == "go_right": return aim, [1, 0]

def FillFireAtMe(x, y, field):
    global fireAtMe
    fireAtMe = [0, 0, 0, 0]
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for i in range(4):
        dx = x + directions[i][0]
        dy = y + directions[i][1]
        while IsAviable(dx, dy):
            if not IsEmpty(dx, dy, field):
                if len(field[dx][dy]) == 0:
                    return
                isFiring, direction = GetAimAndDirection(field[dx][dy]['history'][len(field[dx][dy]['history'])-1])
                if isFiring and (direction[0] == -1*directions[i][0] and direction[1] == -1*directions[i][1]):
                    fireAtMe[i] = field[dx][dy]['life']
                    break
            dx += directions[i][0]
            dy += directions[i][1]


def make_choice(x, y, field):
    global fireAtMe, width, height
    width = len(field)
    height = len(field[0])
    FillFireAtMe(x, y, field)

    return ""

def GetFieldSymbol(a):
    if a == 0:
        return 0
    return a['life']

if __name__ == "__main__":
    anLife = {'life' : 1, 'history' : ["fire_up", "fire_down"]}
    myLife = {'life' : 10, 'history' : ["fire_up", "fire_right"]}
    field = [[0 for i in range(int(20))] for j in range(int(20))]
    field[5][15] = myLife
    field[7][11] = anLife
    field[5][13] = anLife
    field[9][19] = anLife
    field[2][3] = anLife

    print(make_choice(5, 15, field))

    for i in range(height):
        for j in range(width):
            if GetFieldSymbol(field[j][i]) < 10:
                print(GetFieldSymbol(field[j][i]), end=' ')
            else:
                print(GetFieldSymbol(field[j][i]), end='')
        print(end='\n')
    print(end='\n')

    print(fireAtMe)