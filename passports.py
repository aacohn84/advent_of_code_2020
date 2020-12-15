import re

class Field:
    def __init__(self, name, is_valid_fn):
        self.name = name
        self.is_valid = is_valid_fn

def is_valid_passport(passport, req_fields):
    for field in req_fields:
        m = re.search(field.name + r':(.*?)(\s|$)', passport)
        if m is None or not field.is_valid(m.group(1)):
            return False
    return True

def read_passports(filename):
    f = open(filename, 'r')
    return f.readlines()

def get_required_fields_list():
    def year_validation(s, min_val, max_val):
        return s.isnumeric() and min_val <= int(s) <= max_val
    
    def hgt_validation(s):
        m = re.search('([0-9]+)(cm|in)', s)
        if m is not None:
            d, u = int(m.group(1)), m.group(2)
            return u == 'cm' and 150 <= d <= 193 or u == 'in' and 59 <= d <= 76
        else:
            return False

    def hcl_validation(s):
        return re.match('^#([0-9]|[abcdef]){6}$', s)

    def ecl_validation(s):
        return re.match('^(amb|blu|brn|gry|grn|hzl|oth)$', s)

    def pid_validation(s):
        return re.match('^([0-9]{9})$', s)

    return [
        Field('byr', lambda s : year_validation(s, 1920, 2002)),
        Field('iyr', lambda s : year_validation(s, 2010, 2020)),
        Field('eyr', lambda s : year_validation(s, 2020, 2030)),
        Field('hgt', hgt_validation),
        Field('hcl', hcl_validation),
        Field('ecl', ecl_validation),
        Field('pid', pid_validation)
    ]

def main():
    pp_lines = read_passports("passports.txt")
    req_fields = get_required_fields_list()
    pp_start = pp_end = count_valid = 0
    len_lines = len(pp_lines)
    while pp_end <= len_lines:
        if pp_end == len_lines or pp_lines[pp_end] == '\n':
            pp_list = pp_lines[pp_start:pp_end]
            pp_str = ' '.join(pp_list)
            if is_valid_passport(pp_str, req_fields):
                count_valid += 1
            pp_start = pp_end + 1
        pp_end += 1
    print(count_valid)

main()