import random

suits = ["Spades", "Hearts", "Clubs", "Diamonds"] 
suits_values = {"Spades":"\u2664", "Hearts":"\u2661", "Clubs": "\u2667", "Diamonds": "\u2662"}
cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
card_values = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,
                "9":9, "10":10, "J":10, "Q":10, "K":10}

while True:
    msg=input('Enter option to continue')
    if msg=="!bj":
        deck = []
        for suit in suits:
            for card in cards:
                deck.append(suits_values[suit]+card)

        playersum=0
        dealersum=0
        playerhand=[]
        dealerhand=[]

        for i in range(2):
            playercard = random.choice(deck)
            playerhand.append(playercard)
            deck.remove(playercard)
            
        for i in range(2):
            dealercard = random.choice(deck)
            dealerhand.append(dealercard)
            deck.remove(dealercard)
            
        for en in playerhand:
            playersum+=card_values[en[1:]]
        for en in dealerhand:
            dealersum+=card_values[en[1:]]

        if playersum>21:
            for i in playerhand:
                if i[1:]=='A':
                    playersum-=10
                    playerhand.remove(i)
                    playerhand.append(i[0]+'a')
            
        print('dealer - ',dealerhand[0],'\nplayer - ',playerhand)
        
        if playersum==21 and dealersum==21:
            print('dealer - ',dealerhand,'\nplayer - ',playerhand)
            print('tie')
        elif playersum==21:
            print('dealer - ',dealerhand,'\nplayer - ',playerhand)
            print('You won! Blackjack')
        elif dealersum==21:
            print('dealer - ',dealerhand,'\nplayer - ',playerhand)
            print('You lost.')
        else:
            while True:
                inp=input('hit surrender or stay')
                if inp=='hit':
                    card=random.choice(deck)
                    deck.remove(card)
                    playerhand.append(card)
                    if card[1:] != 'A':
                        playersum+=card_values[card[1:]]
                    else:
                        if playersum+11>21:
                            playersum+=1
                        else:
                            playersum+=11
                    print('dealer - ',dealerhand,'\nplayer - ',playerhand)
                    
                    if playersum>21:
                        for i in playerhand:
                            if i[1:]=='A':
                                playersum-=10
                                playerhand.remove(i)
                                playerhand.append(i[0]+'a')
                    if playersum>21:
                        print('You lost.')
                        break
                elif inp=='surrender':
                    #return half the money
                    print('You surrendered')
                    break
                elif inp=='stay':
                    while dealersum<playersum:
                        card=random.choice(deck)
                        deck.remove(card)
                        dealerhand.append(card)
                        dealersum+=card_values[card[1:]]
                        if dealersum>21:
                            for i in dealerhand:
                                if i[1:]=='A':
                                    dealersum-=10
                                    dealerhand.remove(i)
                                    dealerhand.append(i[0]+'a')
                    if dealersum<21:
                        print('dealer - ',dealerhand,'\nplayer - ',playerhand)
                        print('You lost')
                        break
                    else:
                        print('dealer - ',dealerhand,'\nplayer - ',playerhand)
                        print('You won')
                        break
            
                
            
                
