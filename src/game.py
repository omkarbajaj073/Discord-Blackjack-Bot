import random
from utils import play_msg, card_values, get_deck, check_aces, split_msg

class Game:
    
    def __init__(self, channel = None, user = None):
        self.channel = channel
        self.name = user
        self.active = False
        self.dealerhand = []
        self.dealersum = 0
        self.playerhand = []
        self.playersum = 0
        self.deck = get_deck()
        self.has_split = False
        self.can_split = True
        self.active_hands = 1
        self.cur = None
        self.can_surrender = True
    
    
    async def start_game(self):
        
        self.active = True
        for _ in range(2):
            playercard = random.choice(self.deck)
            self.playerhand.append(playercard)
            self.deck.remove(playercard)
        # self.deck.remove('♥K')
        # self.deck.remove('♦K')
        # self.playerhand.append('♥K')
        # self.playerhand.append('♦K')
            
        for _ in range(2):
            dealercard = random.choice(self.deck)
            self.dealerhand.append(dealercard)
            self.deck.remove(dealercard)
            
        for en in self.playerhand:
            self.playersum+=card_values[en[1:]]
        for en in self.dealerhand:
            self.dealersum+=card_values[en[1:]]
        
        if self.playersum==21 and self.dealersum==21:
            await self.show_hands()
            await self.channel.send('It was a tie.')
            self.reset_game()
            return
        elif self.playersum==21:
            await self.show_hands()
            await self.channel.send('You won! Blackjack')
            self.reset_game()
            return
        elif self.dealersum==21:
            await self.show_hands()
            await self.channel.send('You lost. Blackjack')
            self.reset_game()
            return
        
        await self.show_hands(only_first = True)
        
        if self.playerhand[0][1:] == self.playerhand[1][1:]:
            await self.channel.send(split_msg)
            self.can_split = 1
        else:
            await self.channel.send(play_msg)
        
        
    async def split(self):
        self.can_surrender = False
        if self.can_split and len(self.playerhand) == 2:
            self.has_split = True
            self.can_split = False
            card1 = self.playerhand[0]
            card2 = self.playerhand[1]
            val = card_values[card1[1:]]
            self.playerhand.clear()
            self.playerhand = {
                1: [card1],
                2: [card2]                
            }
            self.playersum = {1: val, 2: val}
            self.active_hands = 2
            self.cur = 1
            await self.channel.send("Split complete\n" + play_msg + "\nPlay for Hand 1.")
            await self.show_hands(only_first=True)

        else:
            await self.channel.send("You can't split at this stage of the game.")
        
    
    async def hit(self, hand=None):
        
        self.can_surrender = False
        card=random.choice(self.deck)
        self.deck.remove(card)
        
        if hand is None:
            self.playerhand.append(card)
            self.playersum+=card_values[card[1:]]   
            if self.playersum>21:
                self.check_aces_player()    
            if self.playersum>21:
                await self.channel.send('You lost.')
                await self.show_hands()
                self.reset_game()
                return
                 
        else:
            self.playerhand[hand].append(card)
            self.playersum[hand]+=card_values[card[1:]]
            if self.playersum[hand]>21:
                self.check_aces_player(hand=hand)
            if self.playersum[hand]>21:
                self.active_hands -= 1
                
                if self.active_hands == 0:
                    await self.stay()
                    self.reset_game()
                    return
                    
                await self.channel.send('You lost on Hand ' + str(hand+1))
                await self.show_hands(only_first=True)
                self.cur = (self.cur % 2) + 1    
                return             

        await self.show_hands(only_first=True)   
        if self.active_hands == 2:
            self.cur = (self.cur % 2) + 1
        if self.has_split:
            await self.channel.send("Play for Hand " + str(self.cur))
    
    async def stay(self):
        
        self.active_hands -= 1
        self.can_surrender = False
        if self.active_hands <= 0:
            if self.has_split:
                sm = max(self.playersum[1], self.playersum[2])
                if sm > 21:
                    sm = min(self.playersum[1], self.playersum[2])
            else:
                sm = self.playersum
            while self.dealersum<sm:
                card=random.choice(self.deck)
                self.deck.remove(card)
                self.dealerhand.append(card)
                self.dealersum+=card_values[card[1:]]
                if self.dealersum>21:
                    self.check_aces_dealer()
                    
            if self.dealersum<21:
                msg = 'The dealer won'
                if self.has_split:
                    msg += ' on both hands'
                await self.channel.send(msg)
            elif self.dealersum==sm:
                if not self.has_split:
                    await self.channel.send('It was a tie.')
                else:
                    for i in range(1, 3):
                        if self.dealersum > self.playersum[i] or self.playersum[i] > 21:
                            await self.channel.send("Hand " + str(i+1) + " lost.")
                        else:
                            await self.channel.send("Hand " + str(i+1) + " tied.")
            else:
                if self.has_split:
                    for i in range(1, 3):
                        if self.playersum[i] > 21:
                            await self.channel.send("Hand " + str(i+1) + " lost.")
                        else:
                            await self.channel.send("Hand " + str(i+1) + " won.")
                else:
                    await self.channel.send("You won.")
        
            await self.show_hands()
            self.reset_game()

        else:
            self.cur = (self.cur % 2) + 1
            await self.channel.send("Play for Hand " + str(self.cur))
            
            
    async def surrender(self):
        if self.can_surrender:
            await self.channel.send('You surrendered ' + self.name)
            self.reset_game()
        else:
            await self.channel.send("You can't surrender at this stage in the game.")
        
    
    async def show_hands(self, only_first = False):
        msg = "Dealer - "
        if only_first:
            msg += self.dealerhand[0]
        else:
            for card in self.dealerhand:
                msg += card.upper() + " "
        if not only_first:
            msg += "\nDealer Score - " + str(self.dealersum)
        
        if self.has_split:
            msg += "\nPlayer - Hand 1: "
            for card in self.playerhand[1]:
                msg += card.upper() + " "
            msg += "\nScore on Hand 1 - " + str(self.playersum[1])
            msg += "\nPlayer - Hand 2: "
            for card in self.playerhand[2]:
                msg += card.upper() + " "
            msg += "\nScore on Hand 2 - " + str(self.playersum[2])
        else:
            msg += "\nPlayer - "
            for card in self.playerhand:
                msg += card.upper() + " "
            msg += "\nPlayer Score - " + str(self.playersum)
        
        await self.channel.send(msg)
        
    
    def check_aces_player(self, hand=None):
        if hand is None:
            self.playerhand, self.playersum = check_aces(self.playerhand, self.playersum)
        else:
            self.playerhand[hand], self.playersum[hand] = check_aces(self.playerhand[hand], self.playersum[hand])
    
    
    def check_aces_dealer(self):
        self.dealerhand, self.dealersum = check_aces(self.dealerhand, self.dealersum)
    
    
    def reset_game(self, hand=None):
        if self.active_hands and hand is not None:
            self.playerhand[hand].clear()
            self.playersum[hand] = 0
        else:    
            self.dealerhand.clear()
            self.dealersum = 0
            self.playerhand = []
            self.playersum = 0
            self.deck = get_deck()
            self.active = False
            self.active_hands = 1
            self.can_split = 0
            self.has_split = 0