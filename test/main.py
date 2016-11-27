def make_choice(x, y, field):
    try:
        open("./bots/file.m", 'r')
    except:
        open("./bots/file.m", 'w+')
    return "go_up"
