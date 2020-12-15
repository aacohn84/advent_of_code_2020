def count_trees(slope_map, right, down):
    row = col = 0
    map_width = len(slope_map[0])
    bottom = len(slope_map) - 1
    trees = 0
    while row < bottom:
        col = (col + right) % map_width
        row += down
        if slope_map[row][col] == '#':
            trees += 1
    return trees

def read_map(filename):
    f = open(filename, 'r')
    lines = []
    for l in f:
        lines.append(l.strip())
    return lines

def main():
    slope_map = read_map("map.txt")
    slopes = [
        (1, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]
    product = count_trees(slope_map, 3, 1)
    for slope in slopes:
        product *= count_trees(slope_map, slope[0], slope[1])
    print(product)

main()