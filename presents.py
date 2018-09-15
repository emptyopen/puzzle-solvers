
import copy

class Grid(object):

    def __init__(self, rows):
        self.rows = [[y for y in x] for x in rows.split('/')]

    def swap(self, x1, y1, x2, y2):
        self.rows[x1][y1], self.rows[x2][y2] = self.rows[x2][y2], self.rows[x1][y1]
        self.update()

    def gravity(self):
        cont = True
        while cont:
            cont = False
            for i, row in enumerate(self.rows[:-1]):
                for j, block in enumerate(row):
                    if self.rows[i][j] != ' ' and self.rows[i + 1][j] == ' ':
                        self.swap(i, j, i + 1, j)
                        cont = True

    def explode(self):
        cont = True
        while cont:
            cont = False
            to_delete = set()
            for i, row in enumerate(self.rows):
                for j, cell in enumerate(row[:-2]):
                    if self.rows[i][j] == self.rows[i][j + 1] == self.rows[i][j + 2]:
                        if self.rows[i][j] != ' ':
                            to_delete.add((i, j))
                            to_delete.add((i, j + 1))
                            to_delete.add((i, j + 2))
                            cont = True
            for i, row in enumerate(self.rows[:-2]):
                for j, cell in enumerate(row):
                    if self.rows[i][j] == self.rows[i + 1][j] == self.rows[i + 2][j]:
                        if self.rows[i][j] != ' ':
                            to_delete.add((i, j))
                            to_delete.add((i + 1, j))
                            to_delete.add((i + 2, j))
                            cont = True
            for coord in to_delete:
                self.rows[coord[0]][coord[1]] = ' '

    def update(self):
        while True:
            grid_copy = copy.deepcopy(self.rows)
            self.gravity()
            self.explode()
            if grid_copy == self.rows:
                break

    def print_grid(self):
        print('')
        for row in self.rows:
            print([x for x in row])

    def neighbors(self, x, y):
        n = []
        if x > 0:
            n.append((x - 1, y))
        if x < len(self.rows) - 1:
            n.append((x + 1, y))
        if y > 0:
            n.append((x, y - 1))
        if y < len(self.rows[0]) - 1:
            n.append((x, y + 1))
        return n

    def is_empty(self):
        for row in self.rows:
            for cell in row:
                if cell != ' ':
                    return False
        return True


def coord_gen(x, y):
    for i in range(x):
        for j in range(y):
            yield (i, j)


#G = Grid('     l /     p /     b /     y /   llp /   ryy / rrbbp ')
#G = Grid('   y   /   y   /   b   / yybyy / bbybb / byybb ')
G = Grid('  l   /  p l /  p l /  l p /  p l /  p l ')
G = Grid('  b  /  b  /  r  /  b  /  p  /  brr/byylb/yllpp')
G.print_grid()

original_grid_copy = copy.deepcopy(G.rows)

h = len(G.rows)
w = len(G.rows[0])
'''
for c1 in coord_gen(h, w):
    for coord in G.neighbors(c1[0], c1[1]):
        G.swap(c1[0], c1[1], coord[0], coord[1])
        grid_copy = copy.deepcopy(G.rows)
        for c2 in coord_gen(h, w):
            for coord2 in G.neighbors(c2[0], c2[1]):
                G.swap(c2[0], c2[1], coord2[0], coord2[1])
                if G.is_empty():
                    print('found: {} {} {} {} '.format((c1[1] + 1, h - c1[0]), (coord[1] + 1, h - coord[0]), (c2[1] + 1, h - c2[0]), (coord2[1] + 1, h - coord2[0])))
                G.rows = copy.deepcopy(grid_copy)
        G.rows = copy.deepcopy(original_grid_copy)
'''

import datetime as dt

start = dt.datetime.now()

for c1 in coord_gen(h, w):
    for d1 in G.neighbors(c1[0], c1[1]):
        if G.rows[c1[0]][c1[1]] == G.rows[d1[0]][d1[1]]:
            continue
        if G.rows[c1[0]][c1[1]] == ' ':
            continue
        G.swap(c1[0], c1[1], d1[0], d1[1])
        grid_copy = copy.deepcopy(G.rows)
        for c2 in coord_gen(h, w):
            for d2 in G.neighbors(c2[0], c2[1]):
                if G.rows[c2[0]][c2[1]] == G.rows[d2[0]][d2[1]]:
                    continue
                if G.rows[c2[0]][c2[1]] == ' ':
                    continue
                G.swap(c2[0], c2[1], d2[0], d2[1])
                grid_copy2 = copy.deepcopy(G.rows)
                for c3 in coord_gen(h, w):
                    for d3 in G.neighbors(c3[0], c3[1]):
                        if G.rows[c3[0]][c3[1]] == G.rows[d3[0]][d3[1]]:
                            continue
                        if G.rows[c3[0]][c3[1]] == ' ':
                            continue
                        G.swap(c3[0], c3[1], d3[0], d3[1])
                        grid_copy3 = copy.deepcopy(G.rows)
                        for c4 in coord_gen(h, w):
                            for d4 in G.neighbors(c4[0], c4[1]):
                                if G.rows[c4[0]][c4[1]] == G.rows[d4[0]][d4[1]]:
                                    continue
                                if G.rows[c4[0]][c4[1]] == ' ':
                                    continue
                                G.swap(c4[0], c4[1], d4[0], d4[1])
                                if G.is_empty():
                                    print('found: {} {} {} {} {} {} {} {}'.format((c1[1] + 1, h - c1[0]), (d1[1] + 1, h - d1[0]), (c2[1] + 1, h - c2[0]), (d2[1] + 1, h - d2[0]),  (c3[1] + 1, h - c3[0]), (d3[1] + 1, h - d3[0]), (c4[1] + 1, h - c4[0]), (d4[1] + 1, h - d4[0])))
                                    break
                                G.rows = copy.deepcopy(grid_copy3)
                        G.rows = copy.deepcopy(grid_copy2)
                G.rows = copy.deepcopy(grid_copy)
        G.rows = copy.deepcopy(original_grid_copy)

diff = (dt.datetime.now() - start).seconds
print('took {} seconds'.format(diff))




#
