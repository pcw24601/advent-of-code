from collections import deque
from pprint import pprint

fname = r'20/input.txt'
# fname = r'20/test2.txt'

message_queue = deque()

class Module:
    module_type = 'Module'
    def __init__(self, name, sends_to: list):
        self.name = name
        self.sends_to = sends_to
        self.state = None
        self.output = None

    def __repr__(self):
        return f'{self.module_type}, name={self.name}, output={self.output}, sends to {self.sends_to}'
    
    def add_incoming_connection(self, module):
        # To allow Conjunction to inherit
        pass

    def process(self, message):
        # Send straight through
        self.output = message.contents
        self.send_output()

    def send_output(self):
        # Create messages
        message_queue
        for recipient in self.sends_to:
            message_queue.append(Message(self.name, self.output, recipient))
        

class Conjunction(Module):
    module_type = 'Conjunction'
    def __init__(self, name, sends_to):
        super().__init__(name, sends_to)
        self.state = {}

    def __repr__(self):
        return super().__repr__() + f', state={self.state}, recieves from {list(self.state.keys())}'
 
    def add_incoming_connection(self, module):
        # initialise state to False
        self.state[module.name] = False

    def process(self, message):
        # Send True if all inputs True, else False
        self.state[message.sender] = message.contents
        if sum(self.state.values()) == len(self.state):
            # all inputs high
            self.output = False
        else:
            self.output = True
        self.send_output()


class FlipFlop(Module):
    module_type = 'FlipFlop'

    def process(self, message):
        if message.contents:
            return  # do nothing if high input
        self.output = not self.output
        self.send_output()


class Message:
    high_count = 0
    low_count = 0
    rx_pulses = 0
    def __init__(self, sender: str, contents: bool, recipient):
        self.sender = sender
        self.contents = contents
        self.recipient = recipient

    def __repr__(self):
        return f'Message from {self.sender} sending {self.contents} to {self.recipient} highs={self.high_count}, lows={self.low_count}'

    def process(self):
        # Check for 'rx' being low
        if (self.recipient == 'rx'):
            Message.rx_pulses += 1 + self.contents  # Hack--will be exactly 1 if gets a single False

        if self.contents:
            Message.high_count += 1
        else:
            Message.low_count += 1
        try:
            modules[self.recipient].process(self)
        except KeyError:
            pass


# create modules
modules = {'button': Module('button', ['broadcaster'])}
with open(fname, 'r') as fp:
    lines = fp.readlines()

for ln in lines:
    ThisModule = Module
    name, sends_to = ln.strip().split(' -> ')
    if name.startswith(r'%'):
        ThisModule = FlipFlop
        name = name[1:]
    elif name.startswith(r'&'):
        ThisModule = Conjunction
        name = name[1:]
    sends_to = sends_to.split(', ')

    modules[name] = ThisModule(name, sends_to)

# Set up incoming connections
for module in modules.values():
    for incoming_module in module.sends_to:
        try:
            modules[incoming_module].add_incoming_connection(module)
        except KeyError:
            pass

# pprint(modules)

cache = set()
# for button_presses in range(1000):
button_presses = 0
while True:
    button_presses += 1
    Message.rx_pulses = 0
    message_queue.append(Message('button', False, 'broadcaster'))
    while len(message_queue):
        this_message = message_queue.popleft()
        # print(this_message)
        this_message.process()

    if Message.rx_pulses == 1:
        print(button_presses)
        break

    if button_presses % 100000 == 0:
        print(f'{button_presses=}  {Message.rx_pulses=}')
    
    cached = {module.__repr__ for module in modules}
    if cached in cache:
        print(button_presses)
        break

