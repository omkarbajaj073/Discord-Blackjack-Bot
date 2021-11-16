class Card():
    
    def __init__(self, suit, rank):
        assert suit in ['Spades', 'Hearts', 'Diamonds', 'Clubs'], "Invalid suit"
        self.suit = suit
        self.rank = rank
        
    def __repr__(self):
        return f'{self.suit}: {self.rank}'
    
    def __eq__(self, other):
        return self.rank == other.rank
    
    def __lt__(self, other):
        return
    
    def __gt__(self, other):
        return