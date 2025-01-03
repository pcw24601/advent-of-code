# Process time: 0.000288 seconds.
import re
import time


class Computer:
    def __init__(self, lines: list[str]):
        self.reg_a = int(lines[0].removeprefix('Register A: '))
        self.reg_b = int(lines[1].removeprefix('Register B: '))
        self.reg_c = int(lines[2].removeprefix('Register C: '))
        prog = re.findall('\d', lines[4])
        self.prog = list(map(int, prog))
        self.ins_ptr = 0
        self.output = []

    def combo_op(self, literal_op):
        match literal_op:
            case 0 | 1 | 2 | 3:
                return literal_op
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
            case 7:
                raise RuntimeError('Invalid combo operand')

    def xdv(self, operand):
        return self.reg_a // (2**self.combo_op(operand))

    def perform_op(self, opcode, operand):
        match opcode:
            case 0:
                self.reg_a = self.xdv(operand)
            case 1:
                self.reg_b = self.reg_b ^ operand
            case 2:
                self.reg_b = self.combo_op(operand) % 8
            case 3:
                if self.reg_a:
                    self.ins_ptr = operand
                    return  # don't increment ins_ptr
            case 4:
                self.reg_b ^= self.reg_c
            case 5:
                self.output.append(self.combo_op(operand) % 8)
            case 6:
                self.reg_b = self.xdv(operand)
            case 7:
                self.reg_c = self.xdv(operand)
        self.ins_ptr += 2

    def read_output(self):
        return ','.join(map(str, self.output))

    def run_prog(self):
        while self.ins_ptr < len(self.prog):
            opcode = self.prog[self.ins_ptr]
            operand = self.prog[self.ins_ptr + 1]
            self.perform_op(opcode, operand)
        return self.read_output()


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        lines = fp.read().splitlines()

    computer = Computer(lines)
    print(computer.run_prog())


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
