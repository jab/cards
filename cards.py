#!/usr/bin/env python3

from collections import namedtuple
from functools import total_ordering
from random import shuffle

Suit = namedtuple('Suit', 'id color')
HEARTS = Suit(id='♡', color='red')
DIAMONDS = Suit(id='♢', color='red')
CLUBS = Suit(id='♣', color='black')
SPADES = Suit(id='♠', color='black')
SUITS = (HEARTS, DIAMONDS, CLUBS, SPADES)
NAME_BY_SUIT = {HEARTS: 'HEARTS', DIAMONDS: 'DIAMONDS', CLUBS: 'CLUBS', SPADES: 'SPADES'}

Rank = namedtuple('Rank', 'id')
RANKIDS_ACE_HI = list(range(2, 11)) + ['J', 'Q', 'K', 'A'] # [2, 3, ..., 10, 'J', 'Q', 'K', 'A']
RANKIDS_ACE_LO = [RANKIDS_ACE_HI[-1]] + RANKIDS_ACE_HI[:-1] # ['A', 2, 3, ..., 10, 'J', 'Q', 'K']
INDEX_BY_RANKID_ACE_HI = dict(zip(RANKIDS_ACE_HI, range(2, 15))) # {2: 2, 3: 3, ..., J: 11, Q: 12, K: 13, A: 14}
INDEX_BY_RANKID_ACE_LO = dict(INDEX_BY_RANKID_ACE_HI, A=1) # {A: 1, 2: 2, 3: 3, ..., J: 11, Q: 12, K: 13}
# rank comparison functions, for determining whether e.g. Rank(id='A') < Rank(id='K')
Rank.__eq__ = lambda self, other: self.id == other.id
rank_lt_ace_hi = lambda self, other: INDEX_BY_RANKID_ACE_HI[self.id] < INDEX_BY_RANKID_ACE_HI[other.id]
rank_lt_ace_lo = lambda self, other: INDEX_BY_RANKID_ACE_LO[self.id] < INDEX_BY_RANKID_ACE_LO[other.id]
Rank.__lt__ = rank_lt_ace_hi # choose ace hi by default, easily swapped out though
Rank = total_ordering(Rank)
RANKS = tuple(Rank(id=i) for i in RANKIDS_ACE_HI)
NAME_BY_RANKID = dict(zip(RANKIDS_ACE_HI, ('TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'JACK', 'QUEEN', 'KING', 'ACE')))
# export names for each rank to this module's namespace, so e.g. "TWO" refers to the Rank(id=2) object
locals().update({NAME_BY_RANKID[rank.id]: rank for rank in RANKS})

Card = namedtuple('Card', 'rank suit')
# print cards out like 3♡ instead of Card(Rank(id=3), suit=Suit(id='♡'...
Card.__str__ = lambda self: str(self.rank.id) + str(self.suit.id)
Card.__repr__ = Card.__str__
# give Cards a default ordering, expecting overriding as desired
Card.__eq__ = lambda self, other: self.rank == other.rank and self.suit == other.suit
Card.__lt__ = lambda self, other: self.rank < other.rank if self.suit == other.suit else SUITS.index(self.suit) < SUITS.index(other.suit)
Card = total_ordering(Card)
CARDS = tuple(Card(rank=rank, suit=suit) for suit in SUITS for rank in RANKS)
# export names for each card to this module's namespace, so you can refer to the two of hearts with "TWO_HEARTS"
locals().update({NAME_BY_RANKID[card.rank.id]+'_'+NAME_BY_SUIT[card.suit]: card for card in CARDS})

def new_shuffled_deck():
    '''Create and return a new list of the 52 standard cards in random order.

    >>> deck = new_shuffled_deck()
    >>> len(deck) # no jokers!
    52
    >>> len(set(card.rank for card in deck)) # 13 unique ranks
    13
    >>> len(set(card.suit for card in deck)) # 4 unique suits
    4
    >>> another_deck = new_shuffled_deck()
    >>> deck == another_deck # highly unlikely if our shuffle function is any good
    False
    >>> sorted(deck) == sorted(another_deck)
    True
    '''
    deck = list(CARDS)
    shuffle(deck)
    return deck

if __name__ == '__main__':
    import doctest
    doctest.testmod()