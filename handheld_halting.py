import re

class Instruction:
    def __init__(self, code, value):
        self.code = code
        self.code_backup = code
        self.value = int(value)
        self.executed = False
    
    def __repr__(self):
        return str((self.code, self.value, self.executed))
    
    def is_executed(self):
        return self.executed
    
    def set_executed(self):
        self.executed = True

    def restore(self):
        self.code = self.code_backup

    def correct(self):
        self.code = 'nop' if self.code == 'jmp' else 'jmp'
        self.executed = False

    def is_corrected(self):
        return self.code != self.code_backup

class Execution:
    def __init__(self, instructions_file):
        self.instructions = self.read_instructions(instructions_file)
        self.len_instructions = len(self.instructions)
        self.pc = 0
        self.acc = 0
        self.stack = []
        self.corrected = None
    
    def done(self):
        return self.pc >= self.len_instructions

    def accumulate(self, value):
        self.acc += value
        self.pc += 1

    def rollback_to_last_jump(self):
        while len(self.stack) > 0:
            self.pc = self.stack.pop()
            last_executed = self.get_current_instruction()
            if last_executed.code == 'acc':
                self.accumulate(-last_executed.value)
            elif last_executed.code == 'jmp':
                return

    def rollback_to_last_corrected_instruction(self):
        while len(self.stack) > 0:
            self.pc = self.stack.pop()
            last_executed = self.get_current_instruction()
            if last_executed.is_corrected():
                return
            elif last_executed.code == 'acc':
                self.accumulate(-last_executed.value)

    def jump(self, value):
        self.pc += value

    def nop(self, value):
        # correct this nop if it would lead to immediate program termination
        if not self.is_corrected() and value == self.len_instructions - self.pc:
            self.instructions[self.pc].correct()
        else:
            self.pc += 1

    def is_corrected(self):
        return self.corrected is not None

    def correct_current_instruction(self):
        self.get_current_instruction().correct()
        self.corrected = self.pc

    def restore_current_instruction(self):
        self.get_current_instruction().restore()
        self.corrected = None

    def get_current_instruction(self):
        return self.instructions[self.pc]

    def execute_next_instruction(self):
        ins = self.get_current_instruction()
        if ins.is_executed():
            if self.is_corrected():
                self.rollback_to_last_corrected_instruction()
                self.restore_current_instruction()
            else:
                self.rollback_to_last_jump()
                self.correct_current_instruction()
        else:
            idx = self.pc
            if ins.code == 'acc':
                self.accumulate(ins.value)
            elif ins.code == 'jmp':
                self.jump(ins.value)
            elif ins.code == 'nop':
                self.nop(ins.value)
            ins.set_executed()
            self.stack.append(idx)

    def read_instructions(self, filename):
        f = open(filename, 'r')
        instructions = []
        for l in f:
            m = re.search(r'([a-z]{3}) ([+-][\d]+)', l)
            if m is not None:
                code, value = m.groups(0)[0], m.groups(0)[1]
                instructions.append(Instruction(code, value))
        return instructions

def main():
    execution = Execution("/Users/aaron.cohn/Python/Leetcode/Advent2020/handheld_halting.txt")
    
    while not execution.done():
        execution.execute_next_instruction()
        
    print('acc = ' + str(execution.acc))

main()