import discord

play_msg_text: str = "!hit - Hit me. Ask for another card.\n!stay - stay.\n!surrender - Surrender."
play_msg: discord.Embed = discord.Embed(title='',description=play_msg_text,color=discord.Color.red()) 

help_msg_text = '''**Commands**
!bj <value>: Starts a new game with the player, putting the given amount on the stake. If no amount is entered the default stake amount is used (starts as 500 coins). If the player is playing for the first time, an account is created to store his/her balance (starts as 10,000 coins).
!hit: draw a card
!stay: dealer draws cards
!split: you gets two hands and play seperately for each hand
!continue: in case you do not want to split
!surrender: give up the match
!help: to see rules and commands
!balance: see your game balance
!set <option> <value>: set the default stake (!set bet <value>) or default starting balance (!set start-balance <value>)
!reset: reset your account to the default starting balance. 
Note - this is only valid if you have less than 100 coins

**Rules**
1. A card is dealt to the player facing upwards (visible to everyone).
2. The dealer deals a card to himself visible to everyone. 
3. Another card is given to the player facing upwards.
4. The dealer deals a card facing downwards for himself.
5. The player has to decide whether to hit, stay, split (certain cases) or surrender
6. If the player decides to hit, another card is dealt.
7. If the player decides to stay, then the dealer reveals his hidden card.
8. The dealer has the authority to decide whether to hit or stay.
9. The player has an option to use split, given that he has two cards of same value in the hand
10. If the player decides to split, he gets two hands and plays for these hands seperately.
11. According to the final sum of the cards, the winner is decided.
12. Default bet is 500 coins.
'''
help_msg: discord.Embed = discord.Embed(title='',description=help_msg_text,color=discord.Color.red())

split_msg_text: str = "**Do you want to split?**\n!split - Split.\n!continue - Continue without split\n"
split_msg: discord.Embed = discord.Embed(title='',description=split_msg_text,color=discord.Color.red())

card_values: dict[str, int] = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,
                "9":9, "10":10, "J":10, "Q":10, "K":10}

def get_deck() -> list[str]:
    suits = ['♠', '♥', '♦', '♣']
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = [ suit + card for suit in suits for card in cards ]   
    return deck


def check_aces(hand: list[str], sm: int) -> tuple[list[str], int]:
    for i in hand:
        if i[1:]=='A':
            sm-=10
            hand.remove(i)
            hand.append(i[0]+'a')
        if sm <= 21:
            break
    return hand, sm

      
