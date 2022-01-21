import random
from utils import play_msg, card_values, get_deck, check_aces

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
    
    
    async def start_game(self):
        
        self.active = True
        for _ in range(2):
            playercard = random.choice(self.deck)
            self.playerhand.append(playercard)
            self.deck.remove(playercard)
            
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
        
        msg = "Dealer - "
        msg += self.dealerhand[0] + "\nPlayer - "
        for card in self.playerhand:
            msg += card + " "
        msg += "\nPlayer Score - " + str(self.playersum)
        await self.channel.send(msg)
        await self.channel.send(play_msg)
        
    
    async def hit(self):
        card=random.choice(self.deck)
        self.deck.remove(card)
        self.playerhand.append(card)
        self.playersum+=card_values[card[1:]]        
        
        if self.playersum>21:
            self.check_aces_player()
            
        await self.show_hands(only_first=True)        
        if self.playersum>21:
            await self.channel.send('You lost.')
    
    
    async def stay(self):
        
        while self.dealersum<self.playersum:
            card=random.choice(self.deck)
            self.deck.remove(card)
            self.dealerhand.append(card)
            self.dealersum+=card_values[card[1:]]
            if self.dealersum>21:
                self.check_aces_dealer()
        
        await self.show_hands()
        if self.dealersum<21 and self.dealersum>self.playersum:
            await self.channel.send('The dealer won.')
        elif self.dealersum==self.playersum:
            await self.channel.send('It was a tie.')
        else:
            await self.channel.send('You won.')
        
        self.reset_game()
        
    
    async def surrender(self):
        await self.channel.send('You surrendered ' + self.name)
        self.reset_game()
        
    
    async def show_hands(self, only_first = False):
        msg = "Dealer - "
        if only_first:
            msg += self.dealerhand[0]
        else:
            for card in self.dealerhand:
                msg += card.upper() + " "
        if not only_first:
            msg += "\nDealer Score - " + str(self.dealersum)
        msg += "\nPlayer - "
        for card in self.playerhand:
            msg += card.upper() + " "
        msg += "\nPlayer Score - " + str(self.playersum)
        
        await self.channel.send(msg)
        
    
    def check_aces_player(self):
        self.playerhand, self.playersum = check_aces(self.playerhand, self.playersum)
    
    
    def check_aces_dealer(self):
        self.dealerhand, self.dealersum = check_aces(self.dealerhand, self.dealersum)
    
    
    def reset_game(self):
        self.dealerhand.clear()
        self.dealersum = 0
        self.playerhand.clear()
        self.playersum = 0
        self.deck = get_deck()
        self.active = False
