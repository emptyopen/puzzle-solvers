
import numpy as np
import ast
import urllib2
import json


class Takuzu(object):

    def __init__(self):
        self.table = self.grab_table()
        self.print_table()

    def solve(self):

        max_num = self.puzzle_width / 2

        old_table = np.copy(self.table)
        old_table[0][0] = 'x'
        while not np.array_equal(old_table, self.table):
            old_table = np.copy(self.table)
            for i in range(len(self.table)):

                # solves three in a row
                for j in range(len(self.table[i])):
                    if j <= self.puzzle_width - 3:
                        row_section = self.table[i][j:j+3]
                        if self.num_empty(row_section) == 1:
                            zeros, ones = self.num_ones_zeros(row_section)
                            if zeros == 2:
                                self.table[i][j + np.where(row_section == '.')[0]] = '1'
                            if ones == 2:
                                self.table[i][j + np.where(row_section == '.')[0]] = '0'
                    if i <= self.puzzle_height - 3:
                        col_section = self.table.T[j][i:i+3]
                        if self.num_empty(col_section) == 1:
                            zeros, ones = self.num_ones_zeros(col_section)
                            if zeros == 2:
                                self.table.T[j][i + np.where(col_section == '.')[0]] = '1'
                            if ones == 2:
                                self.table.T[j][i + np.where(col_section == '.')[0]] = '0'

                # solves bit saturation in a row/column
                already = 'x'
                if len([x for x in self.table[i] if x == '0']) == max_num:
                    already = '1'
                if len([x for x in self.table[i] if x == '1']) == max_num:
                    already = '0'
                if already != 'x':
                    for j in range(self.puzzle_width):
                        if self.table[i][j] == '.':
                            self.table[i][j] = already
                already = 'x'
                if len([x for x in self.table.T[i] if x == '0']) == max_num:
                    already = '1'
                if len([x for x in self.table.T[i] if x == '1']) == max_num:
                    already = '0'
                if already != 'x':
                    for j in range(self.puzzle_width):
                        if self.table.T[i][j] == '.':
                            self.table.T[i][j] = already

                # solves 3 spaces left with definite invalid positions
                if self.num_empty(self.table[i]) == 3:
                    num_zeros, num_ones = self.num_ones_zeros(self.table[i])
                    missing_zeros = max_num - num_zeros
                    missing_ones = max_num - num_ones
                    if num_zeros > num_ones:
                        dominant = '1' # dominant means there are more of these bits missing
                    else:
                        dominant = '0'
                    if missing_zeros in [1, 2] and missing_ones in [1, 2]:
                        # if there are two empty spaces and a dominant missing bit adjacent, place dominant missing bit into 3rd empty spot
                        for j in range(len(self.table[i]) - 2):
                            temp_row = self.table[i][j:j + 3]
                            if list(temp_row).count('.') == 2 and dominant in temp_row:
                                indices = np.argwhere(self.table[i] == '.')
                                third_place = [x for x in indices if x not in range(j, j+3)][0][0]
                                self.table[i][third_place] = dominant
                                break
                if self.num_empty(self.table.T[i]) == 3:
                    num_zeros, num_ones = self.num_ones_zeros(self.table.T[i])
                    missing_zeros = max_num - num_zeros
                    missing_ones = max_num - num_ones
                    if num_zeros > num_ones:
                        dominant = '1' # dominant means there are more of these bits missing
                    else:
                        dominant = '0'
                    if missing_zeros in [1, 2] and missing_ones in [1, 2]:
                        # if there are two empty spaces and a dominant missing bit adjacent, place dominant missing bit into 3rd empty spot
                        for j in range(len(self.table.T[i]) - 2):
                            temp_row = self.table.T[i][j:j + 3]
                            if list(temp_row).count('.') == 2 and dominant in temp_row:
                                indices = np.argwhere(self.table.T[i] == '.')
                                third_place = [x for x in indices if x not in range(j, j+3)][0][0]
                                self.table.T[i][third_place] = dominant
                                break

        # now brute force


        self.print_table()


    def char_num(self, c):
        return ord(c) - 96

    def num_ones_zeros(self, row):
        return list(row).count('0'), list(row).count('1')

    def num_empty(self, row):
        return list(row).count('.')

    def grab_table(self):
        if False:
            url = 'https://www.puzzles-mobile.com/binairo/random/6x6-easy/get'
            url = 'https://www.puzzles-mobile.com/binairo/random/8x8-hard/get'
            response = urllib2.urlopen(url)
            html = response.read()
            d = ast.literal_eval(html)
            self.puzzle_width = d['puzzleWidth']
            self.puzzle_height = d['puzzleHeight']
            table_instructions = d['task']
        else:
            table_instructions = 'g00d1d1b1c0h1c1a0g0b0g00b0'
            self.puzzle_width = 8
            self.puzzle_height = 8
        print(table_instructions)
        table = []
        for instruction in table_instructions:
            if instruction.isalpha():
                for _ in range(self.char_num(instruction)):
                    table.append('.')
            else:
                table.append(instruction)
        return np.array(table).reshape((self.puzzle_height, self.puzzle_width))

    def print_table(self):
        for row in self.table:
            print('  ' + ' '.join(row))
        print('\n')


t = Takuzu()

t.solve()















#
