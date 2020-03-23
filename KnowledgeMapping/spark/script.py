def qzfz(origin, actions):
    for a in actions:
        x, y = a
        new_x = y - 1
        new_y = x - 1
        print(new_x, new_y)
        n = abs(origin[new_x][new_y] - 1)
        origin[new_x][new_y] = n
    return origin


s = [[0,0,1,1],[1,0,1,0],[0,1,1,0],[0,0,1,0]]
p = [[2,2],[3,3],[4,4]]
print(qzfz(s, p))

