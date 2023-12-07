import re

fname = r'01a/input.txt'

number_parser = dict(
    one=1,
    two=2,
    three=3,
    four=4,
    five=5,
    six=6,
    seven=7,
    eight=8,
    nine=9
)

regex_list = [re.compile(number_word) for number_word in number_parser.keys()]
regex_list.append(re.compile('\d'))

sum = 0
with open(fname, 'r') as f:
    while ln:=f.readline():
        matches = [list(re.finditer(regex_pattern, ln)) for regex_pattern in regex_list]
        flat_matches = [match for match_list in matches for match in match_list]
        if flat_matches:
            first_match = sorted(flat_matches, key=lambda m: m.span()[0])[0]
            last_match = sorted(flat_matches, key=lambda m: m.span()[1], reverse=True)[0]
            try:
                tens = number_parser[first_match.group()]
            except KeyError:
                tens = int(first_match.group())
            try:
                units = number_parser[last_match.group()]
            except KeyError:
                units = int(last_match.group())
            sum += 10 * tens + units
print(sum)
