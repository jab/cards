#!/usr/bin/env python3.6

from attr import assoc
from cards import *
from collections import Counter
from heapq import nlargest

def replace_rank(*cards, from_=(rAno, rAlo), to=rAhi):
    """

        >>> alo = assoc(cAh, rank=rAlo)
        >>> ahi = assoc(cAs, rank=rAhi)
        >>> check = replace_rank(alo, ahi, from_=(rAhi, rAlo), to=rAno)
        >>> expect = {cAh, cAs}
        >>> check == expect
        True

    """
    return {assoc(c, rank=to) if c.rank in from_ else c for c in cards}

def highestn(*cards, n=5):
    cards = replace_rank(*cards, from_=(rAno, rAlo), to=rAhi)
    cards = nlargest(n, cards)
    cards = replace_rank(*cards, from_=(rAhi,), to=rAno)
    return cards

def best_flush(*cards, n=5):
    """
    Returns the best n-card flush in cards.

    >>> royal = {cAh, cKh, cQh, cJh, c10h}
    >>> cards = royal | {c9h, c8h}
    >>> best_flush(*cards) == royal
    True
    """
    suitcounter = Counter(c.suit for c in cards)
    most_common_suit, nmatching = suitcounter.most_common(1)[0]
    matching = {c for c in cards if c.suit == most_common_suit}
    if nmatching > n:
        return highestn(*matching, n=n)
    if nmatching == n:
        return matching
    return None

if __name__ == '__main__':
    import doctest
    doctest.testmod()
