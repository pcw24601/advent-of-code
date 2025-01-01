# Process time: 0.0107 seconds.
import re
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Gate:
    input1: str
    gate_name: str
    input2: str
    output: str

    def process_gate(self, wires):
        if self.input1 in wires and self.input2 in wires:
            w1 = wires[self.input1]
            w2 = wires[self.input2]
            match self.gate_name:
                case 'OR':
                    wires[self.output] = w1 | w2
                case 'AND':
                    wires[self.output] = w1 & w2
                case 'XOR':
                    wires[self.output] = w1 ^ w2
            return True
        return False


def parse_input(lines: str) -> tuple[dict[str, Optional[int]], set[Gate]]:
    wires = {}
    gates = set()
    initial_wires = re.findall(r'(\w{3}): ([01])', lines)
    for wire_name, wire_state in initial_wires:
        wires[wire_name] = int(wire_state)
    initial_gates = re.findall(r'(\w{3}) (AND|OR|XOR) (\w{3}) -> (\w{3})', lines)
    for gate in initial_gates:
        gates.add(Gate(*gate))
    return wires, gates


def find_output(wires: dict[str, int]) -> int:
    answer = 0
    bit = 0
    while True:
        try:
            next_bit = wires[f'z{bit:02}']
            answer += next_bit * 2 ** bit
            bit += 1
        except KeyError:
            return answer



def main():
    fname = 'input.txt'
    # fname = 'test2.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        lines = fp.read()
    wires, gates = parse_input(lines)
    while gates:
        for gate in gates:
            processed_gates = set()
            if gate.process_gate(wires):
                processed_gates.add(gate)
        gates = gates.difference(processed_gates)

    answer = find_output(wires)
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
