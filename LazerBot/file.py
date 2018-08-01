labyrint = [[1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1],
            [1,1,0,0,1,0,0,1,1],
            [1,0,0,0,0,1,0,0,1],
            [1,1,1,1,0,1,0,1,1],
            [1,1,0,0,0,0,0,1,1],
            [1,1,0,1,0,1,0,1,1],
            [1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1]]
 
def search_neighbors(datlab, x,y): # (функция-костыль)Находит соседние вершины
    value = []
    walks = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
    for walk in walks:
        if datlab[x + walk[0]][y + walk[1]] == 0:
            value.append((x+walk[0],y+walk[1]))
    resultat = {(x,y):value}
    return resultat
 
def search_path(data, x, y, full_path=[], neighbors={}):
    if len(full_path)==0:
        full_path.append((x,y))
    if x==3 and y==7: #(3,7) - точка выхода
        return full_path, neighbors
    else:
        walks = [(-1,0), (0, 1), (1,0), (0,-1)] # up, right, down, left
        for walk in walks:
            if data[x+walk[0]][y+walk[1]] == 0 and ((x+walk[0],y+walk[1]) not in full_path):
                neighbors.update(search_neighbors(data, x, y))
                full_path.append((x+walk[0],y+walk[1]))
                val = search_path(data, x+walk[0],y+walk[1], full_path, neighbors)
                if val != None:
                    return val
                else:
                    full_path.pop()
 
res = search_path(labyrint, 3,1) # точка входа(3, 1)
for val in res[0]:
    labyrint[val[0]][val[1]] = 5
for p in labyrint:
    print(p)