import re
from collections import Counter

fname = r'07/input.txt'
# fname = r'07/test.txt'


conversion_dict = dict(T=10, J=1, Q=12, K=13, A=14)

def value_conversion(hand):
    new_hand = []
    for card in hand:
        try:
            new_card = int(card)
        except ValueError:
            new_card = conversion_dict[card]
        new_hand.append(new_card)
    return new_hand


def score_hand(cards):

    # score highest cards
    cards.reverse()  # won't affect trick score
    cards_score = 0
    for i, card in enumerate(cards):
        cards_score += 15**i * card
        # print(i, card, cards_score)

    # Score tricks
    cards_count = Counter(cards)
    try:
        num_js = cards_count.pop(1)
    except KeyError:
        num_js = 0
    cards_count = sorted(cards_count.values(), reverse=True)
    try:
        cards_count[0] += num_js
    except IndexError:  # hand is JJJJJ
        cards_count = [num_js]

    # print(cards_count)
    if len(cards_count) == 1:
        # 5 of a kind
        trick_score = 7

    elif cards_count[0] == 4:
        # 4 of a kind
        trick_score = 6
    
    elif cards_count[0] == 3:
        if cards_count[1] == 2:
            # full house
            trick_score = 5
        else:
            # 3 of a kind
            trick_score = 4
    elif cards_count[0] == 2:
        if cards_count[1] == 2:
            # 2 pair
            trick_score = 3
        else:
            # pair
            trick_score = 2
    else:
        # high card
        trick_score = 1

    # add in trick score
    cards_score += 15**(i+1) * trick_score

    return cards_score


all_hands = []
with open(fname, 'r') as fp:
    while ln:=fp.readline():
        this_hand = ln.split()
        converted_hand = value_conversion(this_hand[0])
        # in_strs = [[hand, bid] for line in fp.read().split('\n') for (hand, bid) in line.split()]
        # print(converted_hand)
        all_hands.append(dict(converted_hand=converted_hand,
                              bid=int(this_hand[1]))
        )
for hand in all_hands:
    hand['score'] = score_hand(hand['converted_hand'])

scores = sorted([this_hand['score'] for this_hand in all_hands])
ranks = {score: i+1 for i, score in enumerate(scores)}

winnings = 0
for hand in all_hands:
    winnings += hand['bid'] * ranks[hand['score']]


print(winnings)