from copy import deepcopy
import random
import cv2
import numpy

class FloodSolver(object):

    # sequence of colors are in stages (0, 1, 2, 3, 4, ...)

    def __init__(self):

        # brook 3
        self.grid = [['r1', 'g0', 'g0', 'b0', 'b0', 'r0', 'r0', 'g0', 'r0'],
                    ['r1', 'b0', 'g0', 'r0', 'r0', 'g0', 'g0', 'r0', 'r0'],
                    ['b0', 'r0', 'b0', 'r0', 'r0', 'r0', 'b0', 'g0', 'r0'],
                    ['r0', 'b0', 'r0', 'g0', 'b0', 'r0', 'r0', 'b0', 'g0'],
                    ['r0', 'g0', 'r0', 'r0', 'r0', 'g0', 'b0', 'b0', 'b0'],
                    ['g0', 'g0', 'r0', 'b0', 'g0', 'r0', 'g0', 'r0', 'r0'],
                    ['b0', 'b0', 'b0', 'g0', 'b0', 'b0', 'b0', 'r0', 'b0'],
                    ['r0', 'r0', 'r0', 'b0' ,'g0', 'b0', 'b0', 'g0', 'b0'],
                    ['g0', 'r0', 'b0', 'b0', 'b0', 'r0', 'g0', 'b0', 'g0']]
        self.poss_colors = ['r', 'b', 'g']
        self.max_attempts = 9
        self.curr_seq = ['r']

        if False:
            # ocean 1
            self.grid = [['p1', 'a0', 'r0', 'y0', 'a0', 'r0', 'b0', 'y0', 'a0'],
                         ['p1', 'a0', 'g0', 'g0', 'b0', 'g0', 'g0', 'a0', 'g0'],
                         ['a0', 'r0', 'a0', 'g0', 'a0', 'p0', 'y0', 'r0', 'b0'],
                         ['g0', 'r0', 'g0', 'p0', 'b0', 'r0', 'r0', 'a0', 'g0'],
                         ['g0', 'a0', 'a0', 'a0', 'p0', 'r0', 'a0', 'b0', 'a0'],
                         ['a0', 'b0', 'a0', 'b0', 'a0', 'a0', 'a0', 'y0', 'y0'],
                         ['a0', 'y0', 'y0', 'b0', 'p0', 'r0', 'y0', 'b0', 'y0'],
                         ['r0', 'p0', 'r0', 'g0', 'a0', 'r0', 'p0', 'b0', 'a0'],
                         ['b0', 'b0', 'r0', 'y0', 'p0', 'a0', 'b0', 'r0', 'y0']]
            self.poss_colors = ['r', 'b', 'g', 'y', 'a', 'p']
            self.max_attempts = 14
            self.curr_seq = ['p']

        if True:
            self.parse_grid_image('brook53.png')

        self.grid_at = {}
        self.grid_at[0] = deepcopy(self.grid)
        self.already_tried = {i:[] for i in range(self.max_attempts + 1)} # index is the index for curr_seq
        self.active_cells = [0,0]

    def simplify_color(self, rgb):
        b = rgb[0]
        g = rgb[1]
        r = rgb[2]
        if r > 250 and g < 5 and b < 5:
            color = 'r'
        elif r < 5 and g > 250 and b < 5:
            color = 'g'
        elif r < 5 and g < 5 and b > 250:
            color = 'b'
        elif r > 250 and g < 5 and b > 250:
            color = 'p'
        elif r < 5 and g > 250 and b > 250:
            color = 'a'
        elif r > 250 and g > 250 and b < 5:
            color = 'y'
        elif r > 250 and 115 < g < 125 and b < 5:
            color = 'o'
        else:
            color = 'X'
        return color

    def parse_grid_image(self, filename):

        image = cv2.imread(filename)
        print('reading {}'.format(filename))

        # 2960 tall, 1440 wide
        # locations of corners described by: row(814 to 2118), column(69 to 1370)
        # smallest squares approximately 68.5 pixels
        # start 20, 20 in top left corner: 834, 89
        change_locations = []
        last_color = 'none'
        for row in range(834, 2118): # 0 - 2960, vertical
            if self.simplify_color(image[row][80]) != last_color:
                last_color = self.simplify_color(image[row][80])
                change_locations.append(row)

        # total height is 2118 - 814 = 1304, divide and round
        diffs = [change_locations[x] - change_locations[x - 1] for x in range(1, len(change_locations[1:]))][1:]
        diffs = [x for x in diffs if x > 10]
        min_diff = min(diffs)
        single_square_diffs = [x for x in diffs if x < min_diff + 10]
        average_diff = float(sum(single_square_diffs)) / len(single_square_diffs)
        #print('average pixel diff', average_diff)

        num_squares = round(1304 / average_diff)
        #print('num squares', num_squares)

        average_diff = int(round(average_diff))

        self.grid = []
        for row in range(834, 2118, average_diff): # 0 - 2960, vertical
            self.grid.append([])
            for column in range(89, 1370, average_diff): # 0 - 1440, horizontal
                self.grid[-1].append(self.simplify_color(image[row][column]) + '0')
                #grid[-1].append(str(image[row][column]))

        # initialize active cells
        self.grid[0][0] = self.grid[0][0][0] + '1'
        while True:
            self.active_cells = self.find_active_cells()
            curr_grid = deepcopy(self.grid)
            for cell in self.active_cells: # make all connected colors active
                inactive_same_color = self.find_inactive_adjacent_colors(cell[1], cell[0], self.grid[0][0][0]) # for neighbors
                for inactive_cell in inactive_same_color: # update all adjacent colors to be active
                    self.grid[inactive_cell[0]][inactive_cell[1]] = self.grid[0][0][0] + '1'
            if self.grid == curr_grid: # no update was made to grid, continue to next color
                break

        # other initialization
        self.max_attempts = int(raw_input('Max attempts: '))
        self.curr_seq = [self.grid[0][0][0]]

        # find possible colors
        self.poss_colors = []
        for column in range(180, 1440, 180):
            self.poss_colors.append(self.simplify_color(image[2200][column]))
        self.poss_colors = [x for x in self.poss_colors if x != 'X']

        print('possible colors', self.poss_colors)
        print(' ')
        for row in self.grid:
            print(row)



    def find_active_cells(self):
        coords = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j][1] == '1':
                    coords.append([i,j])
        return coords
        # ex. [[1,0], [0,1]]


    def find_inactive_adjacent_colors(self, x, y, color):
        neighbours = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
        return [(b,a) for (a,b) in neighbours if 0 <= b < len(self.grid) and 0 <= a < len(self.grid[b]) and self.grid[b][a] == '{}0'.format(color)]



    def print_grid(self):
        print(' ')
        print('grid @ {} ]]]]]]]]]]]]]]]]]]] active: {}'.format(len(self.curr_seq), len(self.active_cells)))
        print('curr seq: {}'.format(self.curr_seq))
        print(' ')
        for row in self.grid:
            print(row)

    def main(self):

        #print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        #self.print_grid()

        while True:

            #print('\n\n-------------------------')
            #print('already_tried before', self.already_tried)

            # update grid_at for this seq#
            #print('saving grid @ {}'.format(len(self.curr_seq)))
            self.grid_at[len(self.curr_seq) - 1] = deepcopy(self.grid)

            # select color
            possible_colors = [c for c in self.poss_colors if c[0] != self.curr_seq[-1]]
            possible_colors = [c for c in possible_colors if c[0] not in self.already_tried[len(self.curr_seq)]]
            self.color = random.choice(possible_colors)
            self.curr_seq.append(self.color)
            #print('added color to seq:')
            #print('curr_seq', self.curr_seq, len(self.curr_seq))

            # update grid with next color
            cells_to_activate = []
            self.active_cells = self.find_active_cells()
            for cell in self.active_cells: # turn all active cells to the new color
                self.grid[cell[0]][cell[1]] = self.color + '1'
            while True:
                self.active_cells = self.find_active_cells()
                curr_grid = deepcopy(self.grid)
                for cell in self.active_cells: # make all connected colors active
                    inactive_same_color = self.find_inactive_adjacent_colors(cell[1], cell[0], self.color) # for neighbors
                    for inactive_cell in inactive_same_color: # update all adjacent colors to be active
                        self.grid[inactive_cell[0]][inactive_cell[1]] = self.color + '1'
                if self.grid == curr_grid: # no update was made to grid, continue to next color
                    break
            #print('successfully updated grid')

            # show intermediate stage of grid
            #self.print_grid()

            # check if we win
            if len(self.active_cells) == 81:
                break

            # check if we've reached max guesses, if so revert one step
            if len(self.curr_seq) == self.max_attempts + 1:
                #print('out of guesses, moving back one')
                self.already_tried[self.max_attempts].append(self.color)
                self.grid = self.grid_at[self.max_attempts - 1]
                self.curr_seq = self.curr_seq[:-1]
                #self.print_grid()

            # ensure already_tried is in a state where a possible color is guaranteed
            ready_to_break = True
            while ready_to_break:
                ready_to_break = False
                for i in self.already_tried: # check each level
                    if len(self.already_tried[i]) == len(self.poss_colors) - 1: # clear everything above level and add
                        ready_to_break = True
                        #print('found dead end @ level {}'.format(i))
                        for j in range(i, len(self.already_tried)):
                            self.already_tried[j] = []
                        self.already_tried[i - 1].append(self.curr_seq[i - 1])
                        self.curr_seq = self.curr_seq[:-1]
                        self.grid = self.grid_at[i - 2]
                        #self.print_grid()

        # show answer
        for i in range(len(self.curr_seq)):
            print('\n\ngrid @ {}'.format(i))
            for row in self.grid_at[i]:
                print(row)

        print('\n')
        print(self.curr_seq)



F = FloodSolver()
F.main()














##
