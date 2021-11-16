'''
THE BLACKJACK GAME IMPLEMENTATION
'''

def blackjack(cards):
    '''
    Return the value of the hand
    '''
    total = 0
    for card in cards:
        if card.rank == 'Ace':
            total += 11
        elif card.rank in ['King', 'Queen', 'Jack']:
            total += 10
        else:
            total += int(card.rank)
    # Check for aces
    for card in cards:
        if card.rank == 'Ace' and total > 21:
            total -= 10
    return total