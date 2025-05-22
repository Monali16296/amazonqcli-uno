import pygame

class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.hand = []
        self.is_ai = is_ai
    
    def add_card(self, card):
        self.hand.append(card)
        self.sort_hand()
    
    def play_card(self, card_index):
        if 0 <= card_index < len(self.hand):
            return self.hand.pop(card_index)
        return None
    
    def sort_hand(self):
        # Sort cards by color and then by value
        color_order = {"red": 0, "yellow": 1, "green": 2, "blue": 3, "wild": 4}
        
        def sort_key(card):
            # Sort by color first
            color_value = color_order.get(card.color, 5)
            
            # Then by numeric value if possible
            try:
                num_value = int(card.value)
                return (color_value, num_value)
            except ValueError:
                # For non-numeric values, use a string comparison
                # but make sure numbers come before action cards
                return (color_value, 10, card.value)
        
        self.hand.sort(key=sort_key)
    
    def has_playable_card(self, top_card):
        # Check if player has any playable cards
        for card in self.hand:
            if self.is_card_playable(card, top_card):
                return True
        return False
    
    def is_card_playable(self, card, top_card):
        # Wild cards can always be played
        if card.color == "wild":
            return True
        
        # If no top card, any card can be played
        if top_card is None:
            return True
        
        # Match color or value
        if card.color == top_card.color or card.value == top_card.value:
            return True
        
        # If top card is wild, any card can be played (assuming color has been chosen)
        if top_card.color == "wild":
            return True
        
        return False
    
    def ai_play(self, top_card):
        # Simple AI strategy: play the first valid card
        for i, card in enumerate(self.hand):
            if self.is_card_playable(card, top_card):
                return i
        
        # No playable card found
        return -1
    
    def draw_hand(self, surface, x, y, selected_index=-1, is_current_player=False):
        # Draw the player's hand
        card_spacing = 30  # Space between cards
        
        for i, card in enumerate(self.hand):
            # Calculate position
            card_x = x + i * card_spacing
            card_y = y
            
            # If this is the selected card, draw it higher
            if i == selected_index:
                card_y -= 20
            
            # Draw the card
            if is_current_player:
                card.face_up = True
            else:
                card.face_up = False
                
            card.draw(surface, card_x, card_y)
        
        # Draw player name
        font = pygame.font.SysFont('Arial', 20)
        text = font.render(self.name, True, (255, 255, 255))
        surface.blit(text, (x, y - 30))
        
        # Draw card count
        count_text = font.render(f"Cards: {len(self.hand)}", True, (255, 255, 255))
        surface.blit(count_text, (x, y - 50))
        
        # If player has UNO (1 card), display it
        if len(self.hand) == 1:
            uno_font = pygame.font.SysFont('Arial', 30, bold=True)
            uno_text = uno_font.render("UNO!", True, (255, 255, 0))
            surface.blit(uno_text, (x + 100, y - 40))
