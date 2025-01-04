"""
Solve by inspection using this algorithm to find problematic gates.

For each bit that is added, there is an answer bit and a carry bit:

I.e.

Xn | Yn | Cn-1 || Zn | Cn
---+----+------++----+---
0  | 0  |  0   || 0  | 0
1  | 0  |  0   || 1  | 0
0  | 1  |  0   || 1  | 0
1  | 1  |  0   || 0  | 1
0  | 0  |  1   || 1  | 0
1  | 0  |  1   || 0  | 1
0  | 1  |  1   || 0  | 1
1  | 1  |  1   || 1  | 1

Z0 = X0 XOR Y0,
C0 = X0 & Y0

Zn = (Xn XOR Yn) XOR C(n-1)
Cn = ((Xn XOR Yn) & C(n-1)) OR (Xn & Yn)

The code checks for this pattern and prints any discrepancies.
"""

import re
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Gate:
    gate_num: int
    input1: str
    gate_name: str
    input2: str
    output: str

    @property
    def inputs(self):
        return {self.input1, self.input2}


def parse_input(lines: str) -> tuple[dict[str, Optional[int]], set[Gate]]:
    wires = {}
    gates = set()
    initial_wires = re.findall(r'(\w{3}): ([01])', lines)
    for wire_name, wire_state in initial_wires:
        wires[wire_name] = int(wire_state)
    initial_gates = re.findall(r'(\w{3}) (AND|OR|XOR) (\w{3}) -> (\w{3})', lines)
    for gate_num, gate in enumerate(initial_gates):
        gates.add(Gate(gate_num, *gate))
    return wires, gates


def create_dot_str(gates: set[Gate]):
    out_str = 'digraph test {\n'
    str_end = '}'
    for gate in gates:
        out_str += (f'    {{{gate.input1} {gate.input2}}} -> {gate.output} [label="'
                    f'{gate.gate_name}_{gate.gate_num}"]\n')
    out_str += '    subgraph {rank=same'
    for i in range(46):
        out_str += f' x{i:02}'
    out_str += '}\n'
    out_str += '    subgraph {rank=same'
    for i in range(46):
        out_str += f' y{i:02}'
    out_str += '}\n'
    out_str += '    subgraph {rank=same'
    for i in range(47):
        out_str += f' z{i:02}'
    out_str += '}\n'
    return out_str + str_end


def display_mapping(gates: set[Gate]):
    c = {0: 'pgc'}  # by inspection, = x0 AND y0
    swapped_outputs = set()
    for bit in range(1, 45):
        # outputs:
        for gate in gates:
            if {f'x{bit:02}', f'y{bit:02}'} == gate.inputs:
                if gate.gate_name == 'XOR':
                    xxy = gate.output
                elif gate.gate_name == 'AND':
                    xay = gate.output
                else:
                    print(f'Unexpected gate combining X and Y: {gate}')
        for gate in gates:
            if {xxy, c[bit-1]} == gate.inputs:
                if gate.gate_name == 'XOR':
                    zout = gate.output
                    if zout != f'z{bit:02}':
                        print(f'Incorrect output: expected z{bit:02}, got {gate}')
                elif gate.gate_name == 'AND':
                    caxy = gate.output
                else:
                    print(f'Unexpected gate combining c{bit-1:02} and x{bit:02}&y{bit:02}: {gate}')
        for gate in gates:
            if {xay, caxy} == gate.inputs:
                if gate.gate_name == 'OR':
                    c[bit] = gate.output
                else:
                    print(f'Unexpected gate leading to c{bit:02}: {gate}')

        print(f'{bit:02}  x XOR y -> {xxy} XOR c{bit-1:02} ({c[bit-1]}) -> {zout}')
        print(f'    {xxy} AND {c[bit-1]} -> {caxy} OR (X and Y -> {xay}) -> {c[bit]}')
        pass



def main():
    fname = 'input.txt'
    create_dot_file = False

    with open(fname, 'r') as fp:
        lines = fp.read()
    wires, gates = parse_input(lines)

    if create_dot_file:
        # create graphviz file -- create pdf with:
        # sfdp -Tpdf -O -Kdot -Goverlap=false -Gsplines=ortho -Grankdir=RL input.dot
        dot_str = create_dot_str(gates)
        with open(f'{fname.removesuffix(".txt")}.dot', 'w') as fp:
            fp.write(dot_str)

    display_mapping(gates)


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
