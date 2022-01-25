play_msg = "Game started.\n!hit - Hit me.\n!stay - Stay.\n!surrender - Surrender."
help_msg = ""
split_msg = "Do you want to split?\n!split - Split.\n!continue - Continue without split\n"
card_values = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,
                "9":9, "10":10, "J":10, "Q":10, "K":10}

def get_deck():
    suits = ['♠', '♥', '♦', '♣']
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = [ suit + card for suit in suits for card in cards ]   
    return deck


def check_aces(hand, sm):
    for i in hand:
        if i[1:]=='A':
            sm-=10
            hand.remove(i)
            hand.append(i[0]+'a')
        if sm <= 21:
            break
    return hand, sm