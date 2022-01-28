import discord

play_msg_text: str = "!hit - Hit me. Ask for another card.\n!stay - Stay.\n!surrender - Surrender.\n!double - Double the stake"
play_msg: discord.Embed = discord.Embed(title='',description=play_msg_text,color=discord.Color.red()) 

help_msg_text: str = "**!commands: **Displays list of all commands.\n**!rules: **Displays rules of blackjack."
help_msg: discord.Embed = discord.Embed(title='',description=help_msg_text,color=discord.Color.red())

commands_msg_text: str = '''**Commands**
!bj <value>: Starts a new game with the player, putting the given amount on the stake. If no amount is entered the default stake amount is used (starts as 500 coins). If the player is playing for the first time, an account is created to store his/her balance (starts as 10,000 coins).
!hit: Draw a card
!stay: Dealer draws cards
!double: Doubles the stake and deals one card. Then the dealer's hand is revealed.
!split: You get two hands and play separately for each hand
!continue: In case you do not want to split
!surrender: Give up the match. Half the stake will be lost
!help: To see rules and commands
!balance: See your game balance
!set <option> <value>: Set the default stake (!set stake <value>) or default starting balance (!set start-balance <value>)
!view <option> : View the default stake (!view stake) or default starting balance (!view start-balance)
!reset: Reset your account to the default starting balance
Note - !reset is only valid if you have less than 100 coins'''
commands_msg: discord.Embed = discord.Embed(title='',description=commands_msg_text,color=discord.Color.red())

rules_msg_text: str = '''**Rules**
1. The bot deals the dealer and the player a hand of 2 cards. Only the first of the dealer's cards is visible initially.
2. The player can either hit, stay, split (if applicable) or surrender.
3. If the player decides to hit, another card is dealt.
4. If the player decides to stay, then the dealer reveals his hidden card.
5. If the player decides to double down then the player is dealt one card and the dealers hand is checked. The stake is doubled.
6. The player has an option to use split, given that he has two cards of same value in the hand.
7. If the player decides to split, he gets two hands and plays for these hands seperately.
8. If the player doesn't want to split, he/she can use the !continue command.
9. According to the final sum of the cards, the winner is decided.
10. The sum is calculated with the following rules - 
    a. Number cards go by their face value.
    b. Picture cards have a value of 10. 
    c. Aces can have a value of 11, or 1.
11. If the score of a hand is greater than 21, it loses. Otherwise, the higher score wins.'''
rules_msg: discord.Embed = discord.Embed(title='',description=rules_msg_text,color=discord.Color.red())

split_msg_text: str = "**Do you want to split?**\n!split - Split.\n!continue - Continue without split\n"
split_msg: discord.Embed = discord.Embed(title='',description=split_msg_text,color=discord.Color.red())

card_values: dict = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,"9":9, "10":10, "J":10, "Q":10, "K":10}

def get_deck():
    suits = ['♠', '♥', '♦', '♣']
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = [ suit + card for suit in suits for card in cards ]   
    return deck


def check_aces(hand: list, sm: int):
    for i in hand:
        if i[1:]=='A':
            sm-=10
            hand.remove(i)
            hand.append(i[0]+'a')
        if sm <= 21:
            break
    return hand, sm