import cv2
import numpy

image = cv2.imread('flood124.png')

# 2960 tall, 1440 wide

# 1/4 wide is 360

def simplify_color(rgb):
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

#print()

# locations of corners described by: row(814 to 2118), column(69 to 1370)
# smallest squares approximately 68.5 pixels
# start 20, 20 in top left corner: 834, 89
change_locations = []
last_color = 'none'
for row in range(834, 2118): # 0 - 2960, vertical
    if simplify_color(image[row][80]) != last_color:
        last_color = simplify_color(image[row][80])
        change_locations.append(row)

# total height is 2118 - 814 = 1304, divide and round
diffs = [change_locations[x] - change_locations[x - 1] for x in range(1, len(change_locations[1:]))][1:]
diffs = [x for x in diffs if x > 10]
min_diff = min(diffs)
single_square_diffs = [x for x in diffs if x < min_diff + 10]
average_diff = float(sum(single_square_diffs)) / len(single_square_diffs)
print('average pixel diff', average_diff)

num_squares = round(1304 / average_diff)
print('num squares', num_squares)

average_diff = int(round(average_diff))


grid = []
for row in range(834, 2118, average_diff): # 0 - 2960, vertical
    grid.append([])
    for column in range(89, 1370, average_diff): # 0 - 1440, horizontal
        grid[-1].append(simplify_color(image[row][column]))
        #grid[-1].append(str(image[row][column]))

poss_colors = []
for column in range(180, 1440, 180):
    poss_colors.append(simplify_color(image[2200][column]))

print('possible colors', poss_colors)
print(' ')
for row in grid:
    print(row)
