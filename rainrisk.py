import re

"""
curr_angle = arctan(ns_dist / ew_dist)
new_angle = curr_angle + instruction_angle
new_ns_dist = sin(new_angle)
new_ew_dist = cos(new_angle)
"""

class Ship:
    def __init__(self):
        self.orientation = 0 # East
        self.position = (0,0)
        self.waypoint = (10,1)
        self._directions = ['E', 'S', 'W', 'N']

    @staticmethod
    def translate(position, direction, magnitude):
        x, y = position
        if direction == 'N':
            return (x, y + magnitude)
        elif direction == 'S':
            return (x, y - magnitude)
        elif direction == 'E':
            return (x + magnitude, y)
        else:
            return (x - magnitude, y)
    
    def move_to_waypoint(self, moves):
        wx, wy = self.waypoint
        px, py = self.position
        self.position = (px + moves * wx, py + moves * wy)

    def navigate(self, instruction):
        d = instruction.direction
        m = instruction.magnitude
        if d in self._directions:
            self.position = Ship.translate(self.position, d, m)
        elif d == 'R':
            self.rotate_right(m)
        elif instruction.direction == 'L':
            self.rotate_left(m)
        else:
            d = self._directions[self.orientation]
            self.position = Ship.translate(self.position, d, m)

    def navigate_with_waypoint(self, instruction):
        d = instruction.direction
        m = instruction.magnitude
        if d in self._directions:
            self.waypoint = Ship.translate(self.waypoint, d, m)
        elif d == 'R':
            self.rotate_waypoint_right(m)
        elif d == 'L':
            self.rotate_waypoint_left(m)
        else: # d == 'F'
            self.move_to_waypoint(m)

    def rotate_right(self, magnitude):
        self.orientation = (self.orientation + (magnitude // 90)) % 4

    def rotate_waypoint_right(self, angle):
        x, y = self.waypoint
        if angle == 90:
            self.waypoint = (y, -x)
        elif angle == 180:
            self.waypoint = (-x, -y)
        else:
            self.waypoint = (-y, x)

    def rotate_left(self, magnitude):
        self.orientation = (self.orientation - (magnitude // 90)) % 4

    def rotate_waypoint_left(self, angle):
        x, y = self.waypoint
        if angle == 90:
            self.waypoint = (-y, x)
        elif angle == 180:
            self.waypoint = (-x, -y)
        else:
            self.waypoint = (y, -x)

    def manhattan_distance(self):
        return abs(self.position[0]) + abs(self.position[1])

    def __repr__(self):
        return str(self)

    def __str__(self):
        ew_str = 'east' if self.position[0] >= 0 else 'west'
        ns_str = 'north' if self.position[1] >= 0 else 'south'
        ew_mag_str = str(abs(self.position[0]))
        ns_mag_str = str(abs(self.position[1]))
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
        ship.navigate_with_waypoint(instruction)
    print(ship)
    print(ship.manhattan_distance())

main()