#!/usr/bin/env python3
import re

from util import load


class Instruction:
    LINE_REGEX = re.compile(r'^([a-z]+) ([-+0-9]+)$')

    def __init__(self, line):
        m = re.match(self.LINE_REGEX, line)
        if not m:
            raise RuntimeError
        self._op = m.group(1)
        self._arg = int(m.group(2))
        self._executed = False

    def __repr__(self):
        return '(%c) %s %d' % ('*' if self._executed else ' ', self._op, self._arg)

    def set_executed(self, value=True):
        self._executed = value

    def get_executed(self) -> bool:
        return self._executed


class Program:
    def __init__(self, file: str):
        self._program = []
        self._ip = 0
        self._acc = 0
        self.load(file)

    def load(self, file: str):
        lines = load(file)
        self._program = list(map(Instruction, lines))

    def reset(self):
        self._ip = 0
        self._acc = 0
        for instr in self._program:
            instr.set_executed(False)

    def run(self) -> (bool, int):
        ok = False
        while True:
            instr: Instruction = self._program[self._ip]
            # print('IP = %d, ACC = %d, %s' % (self._ip, self._acc, instr))
            if instr.get_executed():
                print('Detected infinite loop! (acc = %d)', self._acc)
                break
            instr.set_executed()
            self._ip += 1
            if 'acc' == instr._op:
                self._acc += instr._arg
            elif 'jmp' == instr._op:
                self._ip += instr._arg - 1
            if self._ip >= len(self._program):
                print('Program terminated! (acc = %d)', self._acc)
                ok = True
                break
        return ok, self._acc

    def fix(self) -> int:
        acc = -1
        for i in range(0, len(self._program)):
            self.reset()
            instr: Instruction = self._program[i]
            if 'acc' == instr._op:
                continue
            is_jmp = 'jmp' == instr._op
            self._program[i]._op = 'nop' if is_jmp else 'jmp'
            ok, acc = self.run()
            self._program[i]._op = 'jmp' if is_jmp else 'nop'
            if ok:
                print('Fixed instruction %d' % i)
                break
        return acc


if __name__ == "__main__":
    program = Program('day8.txt')
    result = program.run()
    assert result == (False, 1801)
    print('Accumulator before infinite loop: %d' % result[1])

    result = program.fix()
    assert result == 2060
    print('Accumulator after normal termination: %d' % result)
