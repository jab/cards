#!/usr/bin/env python3.6

import attr
from attr.validators import instance_of
from random import shuffle

def make_validator(pred):
    def validate(instance, attribute, value):
        if not pred(instance, attribute, value):
            raise ValueError(value)
    return validate

# Implement default Rank semantics: Ace value can be indeterminate (None),
# low (1), or high (14). Non-Ace value can be one of 2, 3, ..., 12 (Q), 13 (K).
# Can easily be overridden if e.g. Ace should have value 1 or 10, and J, Q, K
# should all have value 10.
#
# Ranks are immutable. Create new ones as needed rather than modifying existing ones.
@attr.s(frozen=True, repr=False)
class Rank:
    ACE_NO_VAL = None  # neither hi nor lo
    ACE_LO_VAL = 1
    ACE_HI_VAL = 14
    ACE_VALS = {ACE_NO_VAL, ACE_LO_VAL, ACE_HI_VAL}
    NONACE_VALS = set(range(2, 14))
    VALID_VALS = ACE_VALS | NONACE_VALS
    IDs = tuple(',A,2,3,4,5,6,7,8,9,10,J,Q,K,A'.split(','))
    id = property(lambda self: self.IDs[self.value] if self.value else 'A')
    value = attr.ib(validator=make_validator(lambda i, a, v: v in i.VALID_VALS))
    #__repr__ = lambda self: self.id
    __repr__ = lambda self: 'a' if self.value == self.ACE_LO_VAL else self.id

rAno = Rank(Rank.ACE_NO_VAL)
rAlo = Rank(Rank.ACE_LO_VAL)
rAhi = Rank(Rank.ACE_HI_VAL)

# Default ranks. An alternative set may be used as necessary (e.g. if J, Q, K should all equal 10).
RANKS = {r for r in [rAno] + [Rank(i) for i in range(2, 14)]}

# Suits are immutable. The singleton instances created below should suffice.
@attr.s(frozen=True, repr=False)
class Suit:
    VALID_VALS   = {'hearts',        'diamonds',        'clubs',          'spades'}
    REPR_BY_VAL  = {'hearts': '♡',   'diamonds': '♢',   'clubs': '♣',     'spades': '♠'}
    COLOR_BY_VAL = {'hearts': 'red', 'diamonds': 'red', 'clubs': 'black', 'spades': 'black'}
    value = attr.ib(validator=make_validator(lambda i, a, v: v in i.VALID_VALS))
    color = property(lambda self: self.COLOR_BY_VAL[self.value])
    __repr__ = lambda self: self.REPR_BY_VAL[self.value]

HEARTS   = Suit('hearts')
DIAMONDS = Suit('diamonds')
CLUBS    = Suit('clubs')
SPADES   = Suit('spades')
SUITS    = (HEARTS, DIAMONDS, CLUBS, SPADES)


def to_rank(rank_or_rankval):
    return rank_or_rankval if isinstance(rank_or_rankval, Rank) else Rank(rank_or_rankval)

# Cards are immutable. Create new ones as needed rather than modifying existing ones.
@attr.s(frozen=True, repr=False)
class Card:
    """
    Sorting is by rank and then suit::

        >>> cards = [c7d, c5c, c8s, c8h]
        >>> sorted(cards) == [c5c, c7d, c8h, c8s]
        True

    """
    rank = attr.ib(convert=to_rank, validator=instance_of(Rank))
    suit = attr.ib(validator=instance_of(Suit))
    __repr__ = lambda self: f'[{self.rank!r}{self.suit!r}]'

# Punting on Joker.

# Default cards. Override as necessary. Treat as templates; only modify copies.
CARDS = {Card(r, s) for s in SUITS for r in RANKS}
locals().update({'c%s%s' % (c.rank.id, c.suit.value[0]): c for c in CARDS})


def new_deck(shuffled=True):
    """
    >>> deck = new_deck()
    >>> len(deck)
    52
    >>> len({card.rank for card in deck})  # 13 unique ranks
    13
    >>> len({card.suit for card in deck})  # 4 unique suits
    4
    >>> another_deck = new_deck()
    >>> deck == another_deck  # unlikely
    False
    """
    deck = list(CARDS)
    if shuffled: shuffle(deck)
    return deck


if __name__ == '__main__':
    import doctest
    doctest.testmod()
