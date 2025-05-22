import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.discard_pile = []
        self.create_deck()
        self.shuffle()
    
    def create_deck(self):
        # Create a standard UNO deck
        colors = ["red", "blue", "green", "yellow"]
        
        # Add number cards (0-9) for each color
        for color in colors:
            # One 0 card per color
            self.cards.append(Card(color, "0"))
            
            # Two of each number 1-9 per color
            for value in range(1, 10):
                self.cards.append(Card(color, str(value)))
                self.cards.append(Card(color, str(value)))
            
            # Two of each action card per color
            for action in ["Skip", "Reverse", "Draw2"]:
                self.cards.append(Card(color, action))
                self.cards.append(Card(color, action))
        
        # Add wild cards
        for _ in range(4):
            self.cards.append(Card("wild", "Wild"))
            self.cards.append(Card("wild", "Wild4"))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw_card(self):
        if not self.cards:
            # If deck is empty, shuffle the discard pile and use it as the new deck
            if not self.discard_pile:
                return None  # No cards left in the game
            
            # Keep the top card of the discard pile
            top_card = self.discard_pile.pop()
            
            # Move all other cards from discard pile to deck
            self.cards = self.discard_pile
            self.discard_pile = [top_card]
            
            # Shuffle the new deck
            self.shuffle()
        
        # Draw a card from the deck
        card = self.cards.pop()
        card.load_images()  # Make sure the card has its images loaded
        return card
    
    def add_to_discard(self, card):
        card.face_up = True  # Make sure the card is face up
        self.discard_pile.append(card)
    
    def top_card(self):
        if not self.discard_pile:
            return None
        return self.discard_pile[-1]
    
    def is_playable(self, card):
        # Check if a card can be played on the current top card
        if not self.discard_pile:
            return True  # First card can be anything
        
        top_card = self.top_card()
        
        # Wild cards can always be played
        if card.color == "wild":
            return True
        
        # Match color or value
        if card.color == top_card.color or card.value == top_card.value:
            return True
        
        # If top card is wild, any card can be played (assuming color has been chosen)
        if top_card.color == "wild":
            return True
        
        return False
