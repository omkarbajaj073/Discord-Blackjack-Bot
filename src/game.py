import random
from utils import play_msg, card_values, get_deck, check_aces

class Game:
    
    def __init__(self, channel = None, user = None):
        self.channel = channel
        self.name = user.name
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

        if self.playersum>21:
            self.check_aces_player()
        if self.dealersum>21:
            self.check_aces_dealer()
            
        await self.channel.send('Dealer - ', self.dealerhand[0], '\nPlayer - ', *self.playerhand)
        
        if self.playersum==21 and self.dealersum==21:
            await self.show_hands()
            await self.channel.send('tie')
            return
        elif self.playersum==21:
            await self.show_hands()
            await self.channel.send('You won! Blackjack')
            return
        elif self.dealersum==21:
            await self.show_hands()
            await self.channel.send('You lost.')
            return
        
        await self.channel.send(play_msg)
        
    
    async def hit(self):
        card=random.choice(self.deck)
        self.deck.remove(card)
        self.playerhand.append(card)
        if card[1:] != 'A':
            self.playersum+=card_values[card[1:]]
        else:
            if self.playersum+11>21:
                self.playersum+=1
            else:
                self.playersum+=11
                
        await self.show_hands()
        
        if self.playersum>21:
            for i in self.playerhand:
                if i[1:]=='A':
                    self.playersum-=10
                    self.playerhand.remove(i)
                    self.playerhand.append(i[0]+'a')
                    
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
                
        if self.dealersum<21:
            await self.show_hands()
            await self.channel.send('The dealer won.')
        
        else:
            await self.show_hands()
            await self.channel.send('You won.')
        
        self.reset_game()
        
    
    async def surrender(self):
        await self.channel.send('You surrendered ' + self.user.name)
        self.reset_game()
        
    
    async def show_hands(self):
        msg = "Dealer - "
        for card in self.dealerhand:
            msg += card + " "
        msg += "\nDealer Score - " + str(self.dealerscore) + "\nPlayer - "
        for card in self.playerhand:
            msg += card + " "
        msg += "\nPlayer Score - " + str(self.playerscore)
        
        await self.channel.send(msg)
        
    
    def check_aces_player(self):
        self.playerhand, self.playerscore = check_aces(self.playerhand, self.playerscore)
        # for i in self.playerhand:
        #     if i[1:]=='A':
        #         self.playersum-=10
        #         self.playerhand.remove(i)
        #         self.playerhand.append(i[0]+'a')
        #     if self.playersum <= 21:
        #         break
    
    
    def check_aces_dealer(self):
        self.dealerhand, self.dealerscore = check_aces(self.dealerhand, self.dealerscore)
        # for i in self.dealerhand:
        #     if i[1:]=='A':
        #         self.dealersum-=10
        #         self.dealerhand.remove(i)
        #         self.dealerhand.append(i[0]+'a')
        #     if self.dealersum <= 21:
        #         break

    
    def reset_game(self):
        self.dealerhand.clear()
        self.dealersum = 0
        self.playerhand.clear()
        self.playersum = 0
        self.deck = get_deck()
        self.active = False