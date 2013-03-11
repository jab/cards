from cards import *
from collections import Counter

def flush(*cards):
    '''
    Returns true iff cards are a flush.

    >>> flush(ACE_HEARTS, THREE_HEARTS, FIVE_HEARTS, SEVEN_HEARTS, NINE_HEARTS)
    True
    >>> flush(ACE_HEARTS, THREE_HEARTS, FIVE_HEARTS, SEVEN_HEARTS, NINE_CLUBS)
    False
    '''
    cards = iter(cards)
    first = next(cards).suit
    return all(c.suit == first for c in cards)

def best_flush(*cards):
    '''
    Returns the best 5-card flush in cards.

    >>> royal = [ACE_HEARTS, KING_HEARTS, QUEEN_HEARTS, JACK_HEARTS, TEN_HEARTS]
    >>> cards = royal + [NINE_HEARTS, EIGHT_HEARTS]
    >>> set(best_flush(*cards)) == set(royal)
    True
    >>> best_flush(ACE_CLUBS, TWO_SPADES, THREE_HEARTS, FOUR_SPADES, FIVE_CLUBS)
    '''
    counter = Counter(card.suit for card in cards)
    most_common_suit = counter.most_common(1)[0][0]
    best = sorted(card for card in cards if card.suit == most_common_suit)[-5:]
    return best if len(best) == 5 else None

def straight(*cards):
    '''
    Returns true iff cards are a straight.

    >>> straight(ACE_CLUBS, TWO_HEARTS, THREE_SPADES, FOUR_CLUBS, FIVE_HEARTS)
    True
    >>> straight(ACE_CLUBS, KING_HEARTS, QUEEN_SPADES, JACK_CLUBS, TEN_HEARTS)
    True
    >>> straight(ACE_CLUBS, KING_HEARTS, QUEEN_SPADES, JACK_CLUBS, NINE_HEARTS)
    False
    >>> straight(ACE_CLUBS, KING_HEARTS, QUEEN_SPADES, JACK_CLUBS, JACK_HEARTS)
    False
    '''
    rankids = set(card.rank.id for card in cards)
    l = len(rankids)
    if l != len(cards): return False
    for index_map in (INDEX_BY_RANKID_ACE_HI, INDEX_BY_RANKID_ACE_LO):
        indices = sorted(index_map[rid] for rid in rankids)
        i = indices[0]
        if all(indices[j-i] == j for j in range(i, i+l)):
            return True
    return False

def best_straight(*cards):
    '''
    Returns the best 5-card straight in cards.
    '''
    # TODO

def best_hand(*cards):
    # check for straight flush
    flush = best_flush(*cards)
    if straight(*flush):
        return flush
    # TODO

if __name__ == '__main__':
    import doctest
    doctest.testmod()
