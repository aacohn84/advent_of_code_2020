import re

class Ship:
    def __init__(self):
        self.orientation = 0 # East
        self.position = dict([
            ('E', 0),
            ('S', 0),
            ('W', 0),
            ('N', 0)
        ])
        self._directions = ['E', 'S', 'W', 'N']

    def navigate(self, instruction):
        d = instruction.direction
        m = instruction.magnitude
        if d in self._directions:
            self.position[d] += m
        elif d == 'R':
            self.rotate_right(m)
        elif instruction.direction == 'L':
            self.rotate_left(m)
        else:
            d = self._directions[self.orientation]
            self.position[d] += m

    def rotate_right(self, magnitude):
        self.orientation = (self.orientation + (magnitude // 90)) % 4

    def rotate_left(self, magnitude):
        self.orientation = (self.orientation - (magnitude // 90)) % 4

    def manhattan_distance(self):
        ns_diff = self.position['N'] - self.position['S']
        ew_diff = self.position['E'] - self.position['W']
        return abs(ns_diff) + abs(ew_diff)

    def __repr__(self):
        return str(self)

    def __str__(self):
        ew_str = ''
        if self.position['E'] >= self.position['W']:
            ew_str = 'east'
        else:
            ew_str = 'west'
        ns_str = ''
        if self.position['N'] >= self.position['S']:
            ns_str = 'north'
        else:
            ns_str = 'south'
        ew_mag_str = str(abs(self.position['E'] - self.position['W']))
        ns_mag_str = str(abs(self.position['N'] - self.position['S']))
        return '(' + ew_str + ': ' + ew_mag_str + ', ' + ns_str + ': ' + ns_mag_str + ')'

class ShipInstruction:
    def __init__(self, direction, magnitude):
        self.direction = direction
        self.magnitude = magnitude
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return '(' + self.direction + ', ' + str(self.magnitude) + ')'

def read_instructions(filename):
    f = open(filename, 'r')
    instructions = []
    for l in f:
        m = re.search(r'^([EWNSRLF]){1}(\d+)', l)
        if m is not None:
            instructions.append(ShipInstruction(m.group(1), int(m.group(2))))
    return instructions

def main():
    ship = Ship()
    instructions = read_instructions("/Users/aaron.cohn/Python/Leetcode/Advent2020/rainrisk.txt")
    for instruction in instructions:
        ship.navigate(instruction)
    print(ship)
    print(ship.manhattan_distance())

main()