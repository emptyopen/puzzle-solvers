
import numpy as np
import ast
import urllib2
import json



class Loop(object):

    def __init__(self):
        self.instructions = self.grab_puzzle_instructions()
        self.loop = self.initialize_puzzle_loop()

    def solve(self):
        self.print_puzzle()

        self.x_zeros()
        self.three_x_corner()
        self.fill_4_x()
        self.two_elbow_fill()

        self.print_puzzle()

    def x_zeros(self):
        for i in range(self.puzzle_height):
            for j in range(self.puzzle_width):
                if self.instructions[i][j] == '0':
                    self.update_puzzle(i, j, 0, 'x')
                    self.update_puzzle(i, j, 1, 'x')
                    self.update_puzzle(i + 1, j, 0, 'x')
                    self.update_puzzle(i, j + 1, 1, 'x')

    def three_x_corner(self):
        # fills two loops of a (3) if there is an x-corner
        for i in range(self.puzzle_height):
            for j in range(self.puzzle_width):
                if self.instructions[i][j] == '3':
                    if self.is_x_corner(i, j, 'TL'):
                        self.loop[(i, j)][0] = '-'
                        self.loop[(i, j)][1] = '-'
                    elif self.is_x_corner(i, j, 'BL'):
                        self.loop[(i + 1, j)][0] = '-'
                        self.loop[(i, j)][1] = '-'
                    elif self.is_x_corner(i, j, 'BR'):
                        self.loop[(i + 1, j)][0] = '-'
                        self.loop[(i, j + 1)][1] = '-'
                    elif self.is_x_corner(i, j, 'TR'):
                        self.loop[(i, j)][0] = '-'
                        self.loop[(i, j + 1)][1] = '-'

    def fill_4_x(self):
        # if there are 3 x's around a node, fill the 4th
        for i in range(self.puzzle_height + 1):
            for j in range(self.puzzle_width + 1):
                n_s = self.node_state(i, j)
                if n_s.count('x') == 3 and ' ' in n_s:
                    for c in [(i, j, 0), (i, j, 1), (i - 1, j, 1), (i, j - 1, 0)]:
                        if self.loop[(c[0], c[1])][c[2]] == ' ':
                            self.loop[(c[0], c[1])][c[2]] = 'x'

    def two_elbow_fill(self):
        # if there are two x's around a (2), fill with loops
        for i in range(self.puzzle_height):
            for j in range(self.puzzle_width):
                if self.instructions[i][j] == '2':
                    i_s = self.instruction_state(i, j)
                    print(i, j, i_s)
                    if i_s.count('-') == 2:
                        if (i_s[0] == '-' and i_s[3] == '-') or ('--' in i_s):
                            print(i, j, 'found', i_s)

    def is_x_corner(self, i, j, dir):
        if dir == 'TL':
            if (i, j) == (0, 0): # top left corner
                return True
            if i == 0 and self.loop[(i, j - 1)][0] == 'x': # top row
                return True
            if j == 0 and self.loop[(i - 1, j)][1] == 'x': # left column
                return True
            if self.loop[(i - 1, j)][1] == 'x' and self.loop[(i, j - 1)][0] == 'x': # anywhere else
                return True
        if dir == 'BL':
            if (i, j) == (self.puzzle_height - 1, 0): # bottom left corner
                return True
            if i == self.puzzle_height - 1 and self.loop[(i, j - 1)][0] == 'x': # bottom row
                return True
            if j == 0 and self.loop[(i + 1, j)][1] == 'x': # left column
                return True
            if self.loop[(i + 1, j)][1] == 'x' and self.loop[(i + 1, j - 1)][0] == 'x': # anywhere else
                return True
        if dir == 'BR':
            if (i, j) == (self.puzzle_height - 1, self.puzzle_width - 1): # bottom right corner
                return True
            if i == self.puzzle_height - 1 and self.loop[(i, j + 1)][0] == 'x': # bottom row
                return True
            if j == self.puzzle_width - 1 and self.loop[(i + 1, j)][1] == 'x': # right column
                return True
            if self.loop[(i + 1, j)][1] == 'x' and self.loop[(i, j + 1)][0] == 'x': # anywhere else
                return True
        if dir == 'TR':
            if (i, j) == (0, self.puzzle_width - 1): # top right corner
                return True
            if i == 0 and self.loop[(i, j + 1)][0] == 'x': # top row
                return True
            if j == self.puzzle_width - 1 and self.loop[(i - 1, j)][1] == 'x': # right column
                return True
            if self.loop[(i - 1, j)][1] == 'x' and self.loop[(i, j + 1)][0] == 'x': # anywhere else
                return True
        return False

    def node_state(self, i, j):
        return self.loop[(i - 1, j)][1] + self.loop[(i, j)][0] + self.loop[(i, j)][1] + self.loop[(i, j - 1)][0]

    def instruction_state(self, i, j):
        return self.loop[(i, j)][0] + self.loop[(i, j + 1)][1] + self.loop[(i + 1, j)][0] + self.loop[(i, j)][1]

    def update_puzzle(self, i, j, dir, symb):
        if self.loop[(i, j)][dir] == ' ':
            self.loop[(i, j)][dir] = symb

    def char_num(self, c):
        return ord(c) - 96

    def initialize_puzzle_loop(self):
        size = self.puzzle_width + 1
        d_list = [(x,y) for x in range(-1, size + 1) for y in range(-1, size + 1)]
        d = {x:[' ', ' '] for x in d_list}
        for x in d: # out of bound all set to x
            if x[0] == -1 or x[0] == self.puzzle_width:
                d[x][1] = 'x'
            if x[1] == -1 or x[1] == self.puzzle_height:
                d[x][0] = 'x'
        return d

    def grab_puzzle_instructions(self):
        if False:
            url = 'https://www.puzzles-mobile.com/loop/random/5x5-normal/get'
            response = urllib2.urlopen(url)
            html = response.read()
            d = ast.literal_eval(html)
            self.puzzle_width = d['puzzleWidth']
            self.puzzle_height = d['puzzleHeight']
            puzzle_instructions = d['task']
        else:
            puzzle_instructions = '3b23d12d2b3b202a\n'
            self.puzzle_width = 5
            self.puzzle_height = 5
        print(puzzle_instructions)
        puzzle = []
        for instruction in puzzle_instructions[:-1]:
            if instruction.isalpha():
                for _ in range(self.char_num(instruction)):
                    puzzle.append(' ')
            else:
                puzzle.append(instruction)
        return np.array(puzzle).reshape((self.puzzle_height, self.puzzle_width))

    def print_puzzle(self):
        for i in range(self.puzzle_height):
            # puzzle loop only
            loops_h = []
            loops_v = []
            for j in range(self.puzzle_width + 1):
                if j < self.puzzle_width and self.loop[(i, j)][0] == '-':
                    loops_h.append('---')
                elif j < self.puzzle_width and self.loop[(i, j)][0] == 'x':
                    loops_h.append(' x ')
                else:
                    loops_h.append('   ')
                if i < self.puzzle_height and self.loop[(i, j)][1] == '-':
                    loops_v.append('|')
                elif i < self.puzzle_height and self.loop[(i, j)][1] == 'x':
                    loops_v.append('x')
                else:
                    loops_v.append(' ')
            nodes = ['*' for x in range(self.puzzle_width + 1)]
            loops_h_row = ''.join([x for y in zip(nodes, loops_h) for x in y])
            print(loops_h_row)
            # puzzle loop with instructions
            instructions = self.instructions[i]
            instruction_row = [x for y in zip(loops_v, instructions) for x in y] + [loops_v[-1]]
            print(' '.join(instruction_row))
        # final row
        loops_h = []
        for j in range(self.puzzle_width + 1):
            if j < self.puzzle_width and self.loop[(self.puzzle_height, j)][0] == '-':
                loops_h.append('---')
            elif j < self.puzzle_width and self.loop[(self.puzzle_height, j)][0] == 'x':
                loops_h.append(' x ')
            else:
                loops_h.append('   ')
        nodes = ['*' for x in range(self.puzzle_width + 1)]
        loops_h_row = ''.join([x for y in zip(nodes, loops_h) for x in y])
        print(loops_h_row)
        print('\n')




L = Loop()
L.solve()















#
