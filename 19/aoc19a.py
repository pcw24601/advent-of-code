from pprint import pprint

fname = r'19/input.txt'
# fname = r'19/test.txt'

workflows = {}
parts = []

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
            break  # read all workflows, move on to parts
        workflows = workflows|create_workflow(ln)

    while ln:=fp.readline().strip().strip('{}'):
        categories = ln.split(',')
        parts.append(
            dict(x=int(categories[0][2:]),
            m=int(categories[1][2:]),
            a=int(categories[2][2:]),
            s=int(categories[3][2:]))
        )


# pprint(workflows)
# pprint(parts)

def process_part(part):
    workflow = 'in'
    while True:
        next_workflow = None
        for process in workflows[workflow]:
            if process['test_element'] is None:
                next_workflow = process['output']
                break
            if eval(f'part[process["test_element"]]{process["test_string"]}'):
                next_workflow = process['output']
                break
            
        if next_workflow is None:
            continue

        if next_workflow == 'R':
            return False
        if next_workflow == 'A':
            return True
        workflow = next_workflow



accepted_parts = [part for part in parts if process_part(part)]
print(sum([sum([characteristics for characteristics in part.values()]) for part in accepted_parts]))
      