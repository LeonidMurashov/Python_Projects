import random

def check(x,y,map):
	return x >= 0 and x < len(map[0]) and y >= 0 and y < len(map)

def make_choice(x,y,field):
	actions1 = ["fire_up", "fire_down",
			"fire_left", "fire_right"]
	actions2 = ["go_up","go_right","go_down","go_left"]

	
	if check(x+1,y,field) and field[x+1][y] == 1:
		return actions2[1]

	if check(x,y+1,field) and field[x][y+1] == 1:
		return actions2[0]

	if check(x-1,y,field) and field[x-1][y] == 1:
		return actions2[3]

	if check(x,y-1,field) and field[x][y-1] == 1:
		return actions2[2]

	return random.choice(actions2)
