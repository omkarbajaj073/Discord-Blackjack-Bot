import random
from utils import play_msg, card_values, get_deck, check_aces

class Game:
    
    def __init__(self, channel = None, players = None):
        self.channel = channel
        self.players = players
        self.num_players = len(players)
        self.playerstatus = {}
        self.cur = 0
        
        for player in players:
            self.playerhand[player] = []
            self.playersum[player] = 0
            self.playerstatus[player] = True
        
        self.active = False
        self.dealerhand = []
        self.dealersum = 0
        self.playerhand = {}
        self.playersum = {}
        self.deck = get_deck()
    
    
    async def add_player(self, player):
        self.players.append(player)
        self.num_players += 1
        self.playerhand[player] = []
        self.playersum[player] = 0
        self.playerstatus = True
        await self.channel.send(f"{player} has joined the game.")
    
    
    async def start_game(self):
        
        self.active = True
        for player in self.players:
            for _ in range(2):
                playercard = random.choice(self.deck)
                self.playerhand.append(playercard)
                self.deck.remove(playercard)
            
            for en in self.playerhand:
                self.playersum[player]+=card_values[en[1:]]
            
        for _ in range(2):
            dealercard = random.choice(self.deck)
            self.dealerhand.append(dealercard)
            self.deck.remove(dealercard)
            
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
        await self.channel.send(f"{self.players[self.cur]}'s turn - please play.")
        self.cur += 1
        await self.channel.send(play_msg)
        
    
    async def hit(self, player):
        card=random.choice(self.deck)
        self.deck.remove(card)
        self.playerhand[player].append(card)
        self.playersum[player]+=card_values[card[1:]]        
        
        if self.playersum[player]>21:
            self.check_aces_player()
            
        await self.show_hands(only_first=True)        
        if self.playersum[player]>21:
            await self.channel.send('You lost.')
            self.num_players -= 1
        self.play_next()
    
    
    async def stay(self):
        
        while self.dealersum<self.playersum:
            card=random.choice(self.deck)
            self.deck.remove(card)
            self.dealerhand.append(card)
            self.dealersum+=card_values[card[1:]]
            if self.dealersum>21:
                self.check_aces_dealer()
        self.num_players -= 1
        self.play_next()
            
        
    
    async def surrender(self):
        await self.channel.send('You surrendered ' + self.name)
        self.num_players -= 1
        self.play_next()
        
    
    async def show_hands(self, only_first = False, player = False):
        msg = "Dealer - "
        if only_first:
            msg += self.dealerhand[0]
        else:
            for card in self.dealerhand:
                msg += card.upper() + " "
        if not only_first:
            msg += "\nDealer Score - " + str(self.dealersum)
            
        if player:
            msg += "\n" + player + " - "
            for card in self.playerhand[player]:
                msg += card.upper() + " "
            msg += "\nScore - " + str(self.playersum[player])
        else: 
            for player in self.players:
                msg += "\n" + player + " - "
                for card in self.playerhand[player]:
                    msg += card.upper() + " "
                msg += "\nScore - " + str(self.playersum[player])
        
        await self.channel.send(msg)
        
    
    def check_aces_player(self):
        self.playerhand, self.playersum = check_aces(self.playerhand, self.playersum)
    
    
    def check_aces_dealer(self):
        self.dealerhand, self.dealersum = check_aces(self.dealerhand, self.dealersum)


    def reset_game(self):
        self.dealerhand.clear()
        self.dealersum.clear()
        self.playerhand.clear()
        self.playersum.clear()
        self.players.clear()
        self.deck = get_deck()
        self.active = False
        
        
    async def end_game(self):
        await self.show_hands()
        # Display winnings
        
        
        # old code
        # if self.dealersum<21 and self.dealersum>self.playersum:
        #     await self.channel.send('The dealer won.')
        # elif self.dealersum==self.playersum:
        #     await self.channel.send('It was a tie.')
        # else:
        #     await self.channel.send('You won.')
        
        self.reset_game()
        
        
    async def play_next(self):
        if self.num_players == 0:
            await self.end_game()
        else:
            await self.channel.send(play_msg)
            while not self.playerstatus[self.players[self.cur]]:
                self.cur += 1        

