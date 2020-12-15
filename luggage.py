import re

"""
Baggage Rule Grammar:
<COLOR>  := [a-z]* ' ' [a-z]*
<RULE>      := <COLOR> 'bags contain' <BAG_EXPR> '.' | <COLOR> bags contain no other bags.
<BAG_EXPR>  := <NUMBER> ' ' <COLOR> | <NUMBER> ' ' <COLOR> ', ' <BAG_EXPR>
<NUMBER>    := [0-5]

ex: 
bright white bags contain 1 shiny gold bag.
light red bags contain 1 bright white bag, 2 muted yellow bags.
faded blue bags contain no other bags.
"""

class Bag:
    def __init__(self, color):
        self.color = color
        self.contains_rules = set()
        self.contained_by_rules = set()
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.color
    
    def add_rule(self, contains_bag, quantity):
        new_rule = BagRule(self, contains_bag, quantity)
        self.contains_rules.add(new_rule)
        contains_bag.contained_by_rules.add(new_rule)

class BagRule:
    def __init__(self, bag, contains_bag, quantity):
        self.bag = bag
        self.contains_bag = contains_bag
        self.quantity = quantity
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.bag) + ': ' + str(self.quantity) + 'x ' + str(self.contains_bag)

"""
bag_rule_str: string - non-empty string that conforms to the bag rule grammar
bag_rules: dict{string : BagRule} - dictionary of bag rules keyed by color
"""
def process_bag_rule(bag_rule_str, bags_by_color):
    color_expr = r'^([a-z]* [a-z]*) bags contain'
    no_contain_expr = r'contain no other bags.'
    contains_expr = r'([0-9]) ([a-z]* [a-z]*) bag[s]?'
    
    # get color of this bag and get BagRule if it exists, else create one and add it to the rules
    this_bag_color = re.search(color_expr, bag_rule_str).group(1)
    this_bag = None
    if this_bag_color in bags_by_color:
        this_bag = bags_by_color[this_bag_color]
    else:
        this_bag = Bag(this_bag_color)
        bags_by_color[this_bag_color] = this_bag
    
    # get bags contained by this bag, if any, and set the relationships between them
    m = re.search(no_contain_expr, bag_rule_str)
    if m is None:
        contains_bags = re.findall(contains_expr, bag_rule_str)
        for quantity, color in contains_bags:
            contains_bag = None
            if color in bags_by_color:
                contains_bag = bags_by_color[color]
            else:
                contains_bag = Bag(color)
                bags_by_color[color] = contains_bag
            this_bag.add_rule(contains_bag, int(quantity))

def read_baggage_rules(filename):
    f = open(filename, 'r')
    bag_rules = dict()
    for l in f:
        process_bag_rule(l, bag_rules)
    return bag_rules

def bags_containing_bag(start_bag, accum):
    for rule in start_bag.contained_by_rules:
        if rule.bag not in accum:
            accum.add(rule.bag)
            bags_containing_bag(rule.bag, accum)

def get_bags_containing_color(bag):
    accum = set()
    bags_containing_bag(bag, accum)
    return accum

def get_count_contains(bag):
    sum = 0
    for rule in bag.contains_rules:
        count = get_count_contains(rule.contains_bag)
        sum += rule.quantity + rule.quantity * count
    return sum

def main():
    bags_dict = read_baggage_rules('luggage.txt')
    bag = bags_dict['shiny gold']
    bags_containing_color = get_bags_containing_color(bag)
    count_contains = get_count_contains(bag)
    print('pt 1: ' + str(len(bags_containing_color)))
    print('pt 2: ' + str(count_contains))

main()