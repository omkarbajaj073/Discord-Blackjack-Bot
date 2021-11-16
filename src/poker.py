'''
the poker game implementation
'''

def hand_rank(hand):
    '''
    This function determines the rank of a hand
    '''
    # count the number of each card
    counts = [0] * 14
    for card in hand:
        counts[card.rank] += 1
    # check for a flush
    if len(set([card.suit for card in hand])) == 1:
        return (8, max(counts))
    # check for a straight
    if max(counts) == 1:
        return (7, max(counts))
    
    # check for a straight flush
    
    # check for a full house
    
    # check for a four of a kind
    
    # check for a pair
    
    # check for a three of a kind
    

def poker(hands):
    '''
    This function determines the winner of a poker game
    '''
    # determine the rank of the hands
    ranks = [hand_rank(hand) for hand in hands]
    # sort the hands
    hands = sorted(hands, key=hand_rank)
    # check for a tie
    if hands[0] == hands[1]:
        return 'Tie'
    # return the winner
    return hands[0]