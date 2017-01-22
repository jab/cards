#    def __repr__(self):
#        return '  ②③④⑤⑥⑦⑧⑨⑩ⒿⓆⓀ'[self._val]
#    def __repr__(self):
#        return 'Ⓐ'

def flush(*cards):
    """
    >>> flush(c_A_hearts, c_3_hearts, c_5_hearts, c_7_hearts, c_9_hearts)
    True
    >>> flush(c_A_hearts, c_3_hearts, c_5_hearts, c_7_hearts, c_9_clubs)
    False
    """
    cards = iter(cards)
    firstsuit = next(cards).suit
    return all(c.suit == firstsuit for c in cards)


def reify_aces(*cards, acevals=Rank.ACE_VALS):
    """
    One ace is reified to both lo and hi values::

        >>> ace = c_A_hearts
        >>> other = c_4_clubs
        >>> hand = {ace, other}
        >>> reified = set(frozenset(h) for h in reify_aces(*hand))
        >>> hand_alo = frozenset({assoc(ace, rank=r_A_lo), c_4_clubs})
        >>> hand_ahi = frozenset({assoc(ace, rank=r_A_hi), c_4_clubs})
        >>> reified == {hand_alo, hand_ahi}
        True

    A hand of two aces is reified into all 4 possibilities::

        >>> a1, a2 = c_A_hearts, c_A_clubs
        >>> hand = {a1, a2}
        >>> reified = set(frozenset(h) for h in reify_aces(*hand))
        >>> a1lo = assoc(ace1, rank=r_A_lo)
        >>> a1hi = assoc(ace1, rank=r_A_hi)
        >>> a2lo = assoc(ace2, rank=r_A_lo)
        >>> a2hi = assoc(ace2, rank=r_A_hi)
        >>> lolo = frozenset({a1lo, a2lo})
        >>> lohi = frozenset({a1lo, a2hi})
        >>> hilo = frozenset({a1hi, a2lo})
        >>> hihi = frozenset({a1hi, a2hi})
        >>> reified == {lolo, lohi, hilo, hihi}
        True

    No aces::

        >>> hand = {c_5_hearts, c_4_spades}
        >>> reified = next(reify_aces(*hand))
        >>> reified == hand
        True

    """
    todo = {c for c in cards if not c.rank.value}
    done = {c for c in cards if c.rank.value}
    if not todo:
        yield done
        return
    for card in todo:
        for aceval in acevals:
            reifcard = Card(aceval, card.suit)
            newcards = done | (todo - {card} | {reifcard})
            yield from reify_aces(*newcards, acevals=acevals)


def straight(*cards):
    """
    Returns true iff cards are a straight.

    >>> straight(c_A_clubs, c_2_hearts, c_3_spades, c_4_clubs, c_5_hearts)
    True
    >>> straight(c_A_clubs, c_K_hearts, c_Q_spades, c_J_clubs, c_10_hearts)
    True
    >>> straight(c_A_clubs, c_K_hearts, c_Q_spades, c_J_clubs, c_9_hearts)
    False
    >>> straight(c_A_clubs, c_K_hearts, c_Q_spades, c_J_clubs, c_J_hearts)
    False
    """
    ranks = set(card.rank for card in cards)
    l = len(ranks)
    if l != len(cards): return False
    for index_map in (INDEX_BY_RANKID_ACE_HI, INDEX_BY_RANKID_ACE_LO):
        indices = sorted(index_map[rid] for rid in rankids)
        i = indices[0]
        if all(indices[j-i] == j for j in range(i, i+l)):
            return True
    return False

#def best_straight(*cards):
#    """
#    Returns the best 5-card straight in cards.
#    """
#    # TODO
#
#def best_hand(*cards):
#    # check for straight flush
#    flush = best_flush(*cards)
#    if straight(*flush):
#        return flush
#    # TODO

