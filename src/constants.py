play_msg = "Game started.\n!hit - Hit me.\n!stay - Stay.\n!surrender - Surrender."
help_msg = ""
card_values = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,
                "9":9, "10":10, "J":10, "Q":10, "K":10}

def get_deck():
    deck = []
    suits = ['♠', '♥', '♦', '♣']
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    for suit in suits:
        for card in cards:
            deck.append(suit+card)    
            
    return deck
