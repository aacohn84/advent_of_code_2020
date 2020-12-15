import re
import math

def get_boarding_row(row_code):
    return decipher_code(row_code, 'F', 'B', 127)

def get_boarding_col(col_code):
    return decipher_code(col_code, 'L', 'R', 7)

def decipher_code(code, lower, upper, range):
    lo = 0
    hi = range
    for c in code:
        mid = math.floor((lo / 2) + (hi / 2))
        if c == lower:
            hi = mid
        elif c == upper:
            lo = mid + 1
        else:
            continue
    return lo

def read_boarding_passes(filename):
    f = open(filename, 'r')
    return map(lambda s: s.strip(), f.readlines())

def main():
    boarding_passes = read_boarding_passes('boarding.txt')
    seats = []
    for p in boarding_passes:
        m = re.search(r'([F|B]+)([R|L]+)', p)
        if m is not None:
            row_code = m.group(1)
            col_code = m.group(2)
            row = get_boarding_row(row_code)
            col = get_boarding_col(col_code)
            seat_id = row * 8 + col
            seats.append(seat_id)
    seats = sorted(seats)
    i, j = 0, 1
    last = len(seats)
    while j < last and seats[j] - seats[i] == 1:
        j += 1
        i += 1
    if j < last and seats[j] - seats[i] > 1:
        print(seats[j] - 1)
    else:
        print('seat not found')

main()