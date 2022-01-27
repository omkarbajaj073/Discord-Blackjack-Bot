import discord
import random
from utils import play_msg, card_values, get_deck, check_aces, split_msg

class Game:
    
    def __init__(self, channel = None, user = None, balance = 10000):
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
        self.balance = balance
        self.bet = 0
        self.change = 0
    
    
    async def start_game(self, bet):
        self.bet = bet
        self.active = True
        for i in range(2):
            playercard = random.choice(self.deck)
            self.playerhand.append(playercard)
            self.deck.remove(playercard)
            
        for i in range(2):
            dealercard = random.choice(self.deck)
            self.dealerhand.append(dealercard)
            self.deck.remove(dealercard)
            
        for en in self.playerhand:
            self.playersum+=card_values[en[1:]]
        for en in self.dealerhand:
            self.dealersum+=card_values[en[1:]]
        
        if self.playersum==21 and self.dealersum==21:
            await self.show_hands()
            await self.channel.send('**It was a tie!**')
            await self.reset_game()
            return
        elif self.playersum==21:
            await self.show_hands()
            await self.channel.send('You won! Blackjack')
            await self.channel.send('**You won! Blackjack**')
            self.change += self.bet*3/2
            await self.reset_game()
            return
        elif self.dealersum==21:
            await self.show_hands()
            await self.channel.send('**You lost! Blackjack**')
            self.change -= self.bet
            await self.reset_game()
            return
        
        await self.show_hands(only_first = True)
        
        if card_values[self.playerhand[0][1:]] == card_values[self.playerhand[1][1:]]:
            await self.channel.send(embed=split_msg)
            self.can_split = True
        else:
            await self.channel.send(embed=play_msg)
        
        
    async def split(self):
        self.can_surrender = False
        if self.can_split and len(self.playerhand) == 2:
            self.has_split = True
            self.can_split = False
            card1 = self.playerhand[0]
            card2 = self.playerhand[1]
            card3 = random.choice(self.deck)
            card4 = random.choice(self.deck)
            self.deck.remove(card3)
            self.deck.remove(card4)
            val = card_values[card1[1:]]
            self.playerhand.clear()
            self.playerhand = {
                1: [card1, card3],
                2: [card2, card4]                
            }
            self.playersum = {
                1: val + card_values[card3[1:]], 
                2: val + card_values[card4[1:]]
            }
            self.active_hands = 2
            self.cur = 1
            await self.channel.send("**Split complete!**")
            await self.show_hands(only_first=True)
            await self.channel.send(embed=play_msg)
            await self.channel.send("Play for Hand 1")

        else:
            await self.channel.send("**You can't split at this stage of the game.**")
            
            
    async def cont(self):
        self.can_split = False
        await self.show_hands(only_first=True)
        await self.channel.send("**Continuing game with no split\n**")
        await self.channel.send(embed=play_msg)
        
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
                self.change -= self.bet
                await self.channel.send('**You went over 21. You lost!**')
                await self.show_hands()
                await self.reset_game()
                return
                 
        else:
            self.playerhand[hand].append(card)
            self.playersum[hand]+=card_values[card[1:]]
            if self.playersum[hand]>21:
                self.check_aces_player(hand=hand)
            if self.playersum[hand]>21:
                self.active_hands -= 1
                
                if self.active_hands == 0:
                    await self.stand()
                    await self.reset_game()
                    return
                    
                await self.channel.send('**You lost on Hand**' + str(hand+1))
                await self.show_hands(only_first=True)
                self.cur = (self.cur % 2) + 1    
                return             

        await self.show_hands(only_first=True)   
        if self.active_hands == 2:
            self.cur = (self.cur % 2) + 1
        if self.has_split:
            await self.channel.send("Play for Hand" + str(self.cur))
    

    async def stand(self):
        
        self.change = 0
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
                    
            if self.dealersum<=21 and self.dealersum>sm:
                msg = '**The dealer won!**'
                if self.has_split:
                    msg += '** On both hands!**'
                    self.change -= self.bet
                await self.channel.send(msg)
                self.change -= self.bet
            elif self.dealersum==sm:
                if not self.has_split:
                    await self.channel.send('**It was a tie!**')
                else:
                    for i in range(1, 3):
                        if self.dealersum > self.playersum[i] or self.playersum[i] > 21:
                            await self.channel.send(f"**Hand {i} lost!**")
                            self.change -= self.bet
                        else:
                            await self.channel.send(f"**Hand {i} tied!**")
            else:
                if self.has_split:
                    for i in range(1, 3):
                        if self.playersum[i] > 21:
                            await self.channel.send(f"**Hand {i} lost!**")
                            self.change -= self.bet
                        else:
                            await self.channel.send(f"**Hand {i} won!**")
                            self.change += self.bet
                else:
                    await self.channel.send('**You won!**')
                    self.change += self.bet
        
            await self.show_hands()
            await self.reset_game()

        else:
            self.cur = (self.cur % 2) + 1
            await self.channel.send(f"Play for Hand {self.cur}")
            
            
    async def surrender(self):
        if self.can_surrender:
            await self.channel.send(f'**You surrendered {self.name}.**')
            await self.show_hands()
            self.change -= self.bet/2
            await self.reset_game()
        else:
            await self.channel.send("**You can't surrender at this stage in the game.**")
        
    
    async def show_hands(self, only_first = False):
        msg = "**Dealer - **"
        if only_first:
            msg += self.dealerhand[0]
        else:
            for card in self.dealerhand:
                msg += card.upper() + " "
        if not only_first:
            msg += "\nDealer Score - " + str(self.dealersum)
        
        if self.has_split:
            msg += "**\nPlayer - Hand 1: **"
            for card in self.playerhand[1]:
                msg += card.upper() + " "
            msg += "\nScore on Hand 1 - " + str(self.playersum[1])
            msg += "**\nPlayer - Hand 2: **"
            for card in self.playerhand[2]:
                msg += card.upper() + " "
            msg += "\nScore on Hand 2 - " + str(self.playersum[2])
        else:
            msg += "**\nPlayer - **"
            for card in self.playerhand:
                msg += card.upper() + " "
            msg += "\nPlayer Score - " + str(self.playersum)
        embed=discord.Embed(title=self.name,description=msg,color=discord.Color.red())
        await self.channel.send(embed=embed)
        
    
    def check_aces_player(self, hand=None):
        if hand is None:
            self.playerhand, self.playersum = check_aces(self.playerhand, self.playersum)
        else:
            self.playerhand[hand], self.playersum[hand] = check_aces(self.playerhand[hand], self.playersum[hand])
    
    
    def check_aces_dealer(self):
        self.dealerhand, self.dealersum = check_aces(self.dealerhand, self.dealersum)
    
    
    async def reset_game(self):
        self.balance += self.change
        if self.change < 0:
            self.change *= (-1)
            await self.channel.send(f"You lost {self.change} coins")
        elif self.change == 0:
            await self.channel.send("You gained and lost nothing.")
        else:
            await self.channel.send(f"You won {self.change} coins")
        await self.channel.send("Your current balance is " + str(self.balance))
        
        self.dealerhand.clear()
        self.dealersum = 0
        self.playerhand = []
        self.playersum = 0
        self.deck = get_deck()
        self.active = False
        self.active_hands = 1
        self.can_split = 0
        self.has_split = 0
        self.can_surrender = True
        self.bet = 0
        self.change = 0
