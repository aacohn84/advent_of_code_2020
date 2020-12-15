def get_answers_by_group(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    answer_group = []
    answers_by_group = []
    for l in lines:
        if l == '\n':
            answers_by_group.append(answer_group)
            answer_group = []
        else:
            answer_group.append(l.strip())
    answers_by_group.append(answer_group)
    return answers_by_group

def marked_yes_by_any(ans):
    yes_set = set()
    for c in ans:
        yes_set.add(c)
    return len(yes_set)

def marked_yes_by_all(ans_group):
    ans_sets = []
    for ans in ans_group:
        ans_set = set()
        for c in ans:
            ans_set.add(c)
        ans_sets.append(ans_set)
    all_yes = ans_sets[0].intersection(*ans_sets[1:])
    return len(all_yes)

def main():
    answers = get_answers_by_group('customs.txt')
    sum_yes = 0
    nums_yes = []
    for ans in answers:
        num_yes = marked_yes_by_all(ans)
        sum_yes += num_yes
        nums_yes.append(num_yes)
    print(sum_yes)

main()