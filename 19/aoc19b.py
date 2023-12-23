from pprint import pprint
from copy import deepcopy

fname = r'19/input.txt'
# fname = r'19/test.txt'

workflows = {}

def create_workflow(ln):
    name, remainder = ln.strip('}').split('{')
    processes = remainder.split(',')
    this_process = []
    for process in processes:
        *test_list, output = process.split(':')
        test_element = test_string = None
        if test_list:  # not just output
            test = test_list[0]
            test_element = test[0]
            test_string = test[1:]
        this_process.append(
            dict(test_element=test_element, test_string=test_string, output=output))
    return {name: this_process}
        

with open(fname, 'r') as fp:
    while ln:=fp.readline().strip():
        if len(ln) == 0:
            break  # read all workflows, discard parts
        workflows = workflows|create_workflow(ln)


# pprint(workflows)

process_range=dict(
    x={'min':1, 'max':4000},  # inclusive range
    m={'min':1, 'max':4000},
    a={'min':1, 'max':4000},
    s={'min':1, 'max':4000},    
)

accepted_ranges = []
rejected_ranges = []

def process_tree(process_range, workflow='in'):
    if workflow == 'A':
        accepted_ranges.append(process_range)
        return
    elif workflow == 'R':
        rejected_ranges.append(process_range)
        return

    for process in workflows[workflow]:
        if process['test_element'] is None:
            process_tree(process_range, process['output'])  # could be 'A', 'R', or workflow name
            return
            
        else:
            # split process_range and recursive call on positive branch
            range_passed = deepcopy(process_range)
            test_element = process['test_element']
            test_comparrison = process['test_string'][0]
            test_value = int(process['test_string'][1:])
            range_value = process_range[test_element]

            if test_comparrison == '>':
                if (range_value['min'] < test_value) & (range_value['max'] >= test_value):
                    # split range
                    range_passed[test_element]['min'] = test_value + 1
                    process_range[test_element]['max'] = test_value
                    process_tree(range_passed, process['output'])

            if test_comparrison == '<':
                if (range_value['max'] > test_value) & (range_value['min'] <= test_value):
                    # split range
                    range_passed[test_element]['max'] = test_value - 1
                    process_range[test_element]['min'] = test_value
                    process_tree(range_passed, process['output'])

            if process_range[test_element]['min'] > process_range[test_element]['max']:
                # check--nothing left in range
                return
            # continue with this loop for negative branch

    print('Should never reach here')
    

process_tree(process_range)

# pprint(accepted_ranges)

def mult_list(list_):
    ans = 1
    for x in list_:
        ans *= x
    return ans

# test
# print(mult_list([3,4,10]))

total = 0
for process_range in accepted_ranges:
    total += mult_list([element['max'] - element['min'] + 1 for element in process_range.values()])

print(total)