import pygame
import sys
import time
from deck import Deck
from player import Player

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (50, 50, 80)

class Game:
    def __init__(self):
        pygame.init()
        
        # Set up the display
        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("UNO Game")
        
        # Load fonts
        self.font = pygame.font.SysFont('Arial', 24)
        self.large_font = pygame.font.SysFont('Arial', 36)
        
        # Game state
        self.deck = Deck()
        self.players = []
        self.current_player = 0
        self.direction = 1  # 1 for clockwise, -1 for counter-clockwise
        self.game_over = False
        self.winner = None
        self.selected_card = -1
        self.color_selection = False
        self.chosen_color = None
        
        # Animation variables
        self.animation_active = False
        self.animation_card = None
        self.animation_start_pos = (0, 0)
        self.animation_end_pos = (0, 0)
        self.animation_progress = 0
        self.animation_speed = 0.05
        
        # Sound effects
        pygame.mixer.init()
        try:
            self.card_play_sound = pygame.mixer.Sound("../assets/card_play.wav")
            self.card_draw_sound = pygame.mixer.Sound("../assets/card_draw.wav")
            self.uno_sound = pygame.mixer.Sound("../assets/uno.wav")
            self.win_sound = pygame.mixer.Sound("../assets/win.wav")
        except:
            print("Sound files not found. Continuing without sound.")
            self.card_play_sound = None
            self.card_draw_sound = None
            self.uno_sound = None
            self.win_sound = None
    
    def setup_game(self, num_players=4):
        # Create players (1 human, rest AI)
        self.players = [Player("You", is_ai=False)]
        
        for i in range(1, num_players):
            self.players.append(Player(f"AI {i}", is_ai=True))
        
        # Deal 7 cards to each player
        for _ in range(7):
            for player in self.players:
                card = self.deck.draw_card()
                if card:
                    player.add_card(card)
        
        # Place first card on discard pile
        first_card = self.deck.draw_card()
        
        # If first card is a wild card, assign it a random color
        if first_card.color == "wild":
            colors = ["red", "blue", "green", "yellow"]
            first_card.color = colors[0]  # Just use red for simplicity
        
        self.deck.add_to_discard(first_card)
    
    def next_player(self):
        self.current_player = (self.current_player + self.direction) % len(self.players)
    
    def handle_special_card(self, card):
        if card.value == "Skip":
            self.next_player()  # Skip the next player
        elif card.value == "Reverse":
            self.direction *= -1  # Reverse direction
            if len(self.players) == 2:
                self.next_player()  # In 2-player game, reverse acts like skip
        elif card.value == "Draw2":
            next_player_idx = (self.current_player + self.direction) % len(self.players)
            # Draw 2 cards for the next player
            for _ in range(2):
                new_card = self.deck.draw_card()
                if new_card:
                    self.players[next_player_idx].add_card(new_card)
            self.next_player()  # Skip the next player
        elif card.value == "Wild4":
            next_player_idx = (self.current_player + self.direction) % len(self.players)
            # Draw 4 cards for the next player
            for _ in range(4):
                new_card = self.deck.draw_card()
                if new_card:
                    self.players[next_player_idx].add_card(new_card)
            self.next_player()  # Skip the next player
    
    def play_card(self, card_index):
        player = self.players[self.current_player]
        card = player.play_card(card_index)
        
        if card:
            # Play sound
            if self.card_play_sound:
                self.card_play_sound.play()
            
            # Check for UNO
            if len(player.hand) == 1 and self.uno_sound:
                self.uno_sound.play()
            
            # Add card to discard pile
            self.deck.add_to_discard(card)
            
            # Handle special cards
            self.handle_special_card(card)
            
            # Check for win condition
            if len(player.hand) == 0:
                self.game_over = True
                self.winner = player
                if self.win_sound:
                    self.win_sound.play()
                return
            
            # If wild card was played, player needs to choose a color
            if card.color == "wild":
                self.color_selection = True
            else:
                self.next_player()
    
    def draw_card_for_player(self):
        player = self.players[self.current_player]
        card = self.deck.draw_card()
        
        if card:
            # Play sound
            if self.card_draw_sound:
                self.card_draw_sound.play()
                
            player.add_card(card)
            
            # Check if the drawn card can be played
            if self.deck.is_playable(card):
                # In a real game, player would have the option to play the drawn card
                # For simplicity, we'll just move to the next player
                pass
            
            self.next_player()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Only handle events if it's the human player's turn and no animation is active
            if self.current_player == 0 and not self.animation_active:
                player = self.players[self.current_player]
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle color selection if needed
                    if self.color_selection:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        
                        # Check if a color button was clicked
                        button_width = 100
                        button_height = 50
                        button_y = self.height // 2
                        
                        # Red button
                        if self.width // 2 - 220 <= mouse_x <= self.width // 2 - 120 and button_y <= mouse_y <= button_y + button_height:
                            self.deck.top_card().color = "red"
                            self.color_selection = False
                            self.next_player()
                        
                        # Blue button
                        elif self.width // 2 - 110 <= mouse_x <= self.width // 2 - 10 and button_y <= mouse_y <= button_y + button_height:
                            self.deck.top_card().color = "blue"
                            self.color_selection = False
                            self.next_player()
                        
                        # Green button
                        elif self.width // 2 + 10 <= mouse_x <= self.width // 2 + 110 and button_y <= mouse_y <= button_y + button_height:
                            self.deck.top_card().color = "green"
                            self.color_selection = False
                            self.next_player()
                        
                        # Yellow button
                        elif self.width // 2 + 120 <= mouse_x <= self.width // 2 + 220 and button_y <= mouse_y <= button_y + button_height:
                            self.deck.top_card().color = "yellow"
                            self.color_selection = False
                            self.next_player()
                    
                    else:
                        # Check if a card in the player's hand was clicked
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        card_width = 100
                        card_height = 150
                        card_spacing = 30
                        
                        # Calculate the position of the player's hand
                        hand_x = self.width // 2 - (len(player.hand) * card_spacing) // 2
                        hand_y = self.height - card_height - 20
                        
                        for i in range(len(player.hand)):
                            card_x = hand_x + i * card_spacing
                            
                            # Check if this card was clicked
                            if card_x <= mouse_x <= card_x + card_width and hand_y <= mouse_y <= hand_y + card_height:
                                # Check if the card can be played
                                if player.is_card_playable(player.hand[i], self.deck.top_card()):
                                    # Start animation
                                    self.animation_active = True
                                    self.animation_card = player.hand[i]
                                    self.animation_start_pos = (card_x, hand_y)
                                    self.animation_end_pos = (self.width // 2 - card_width // 2, self.height // 2 - card_height // 2)
                                    self.animation_progress = 0
                                    self.selected_card = i
                                break
                        
                        # Check if the draw pile was clicked
                        draw_pile_x = self.width // 2 - 150
                        draw_pile_y = self.height // 2 - card_height // 2
                        
                        if draw_pile_x <= mouse_x <= draw_pile_x + card_width and draw_pile_y <= mouse_y <= draw_pile_y + card_height:
                            self.draw_card_for_player()
                
                elif event.type == pygame.KEYDOWN:
                    # Select cards with number keys
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        card_idx = event.key - pygame.K_1
                        if card_idx < len(player.hand):
                            if player.is_card_playable(player.hand[card_idx], self.deck.top_card()):
                                self.selected_card = card_idx
                                
                                # Start animation
                                card_spacing = 30
                                hand_x = self.width // 2 - (len(player.hand) * card_spacing) // 2
                                hand_y = self.height - 150 - 20
                                card_x = hand_x + card_idx * card_spacing
                                
                                self.animation_active = True
                                self.animation_card = player.hand[card_idx]
                                self.animation_start_pos = (card_x, hand_y)
                                self.animation_end_pos = (self.width // 2 - 50, self.height // 2 - 75)
                                self.animation_progress = 0
                    
                    # Play selected card with Enter
                    elif event.key == pygame.K_RETURN:
                        if 0 <= self.selected_card < len(player.hand):
                            if player.is_card_playable(player.hand[self.selected_card], self.deck.top_card()):
                                # Start animation
                                card_spacing = 30
                                hand_x = self.width // 2 - (len(player.hand) * card_spacing) // 2
                                hand_y = self.height - 150 - 20
                                card_x = hand_x + self.selected_card * card_spacing
                                
                                self.animation_active = True
                                self.animation_card = player.hand[self.selected_card]
                                self.animation_start_pos = (card_x, hand_y)
                                self.animation_end_pos = (self.width // 2 - 50, self.height // 2 - 75)
                                self.animation_progress = 0
                    
                    # Draw card with D key
                    elif event.key == pygame.K_d:
                        self.draw_card_for_player()
    
    def update_animation(self):
        if self.animation_active:
            self.animation_progress += self.animation_speed
            
            if self.animation_progress >= 1:
                self.animation_active = False
                self.play_card(self.selected_card)
                self.selected_card = -1
    
    def ai_turn(self):
        if self.current_player != 0 and not self.animation_active and not self.color_selection:
            player = self.players[self.current_player]
            
            # Add a small delay to make AI turns visible
            pygame.time.delay(500)
            
            # AI plays a card
            card_idx = player.ai_play(self.deck.top_card())
            
            if card_idx >= 0:
                # AI has a playable card
                self.play_card(card_idx)
                
                # If AI played a wild card, choose a color
                if self.color_selection:
                    # Simple strategy: choose the most common color in hand
                    color_counts = {"red": 0, "blue": 0, "green": 0, "yellow": 0}
                    
                    for card in player.hand:
                        if card.color in color_counts:
                            color_counts[card.color] += 1
                    
                    # Find the most common color
                    max_count = 0
                    chosen_color = "red"  # Default
                    
                    for color, count in color_counts.items():
                        if count > max_count:
                            max_count = count
                            chosen_color = color
                    
                    # Set the color of the wild card
                    self.deck.top_card().color = chosen_color
                    self.color_selection = False
                    self.next_player()
            else:
                # AI has no playable card, draw one
                self.draw_card_for_player()
    
    def draw_game(self):
        # Fill the background
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw the deck and discard pile
        card_width = 100
        card_height = 150
        
        # Draw pile (face down)
        if self.deck.cards:
            pygame.draw.rect(self.screen, (0, 0, 100), (self.width // 2 - 150, self.height // 2 - card_height // 2, card_width, card_height))
            pygame.draw.rect(self.screen, WHITE, (self.width // 2 - 150 + 5, self.height // 2 - card_height // 2 + 5, card_width - 10, card_height - 10), 2)
            
            # Draw UNO text on the draw pile
            draw_text = self.font.render("UNO", True, WHITE)
            self.screen.blit(draw_text, (self.width // 2 - 150 + 30, self.height // 2 - 15))
        
        # Discard pile (top card face up)
        top_card = self.deck.top_card()
        if top_card:
            top_card.draw(self.screen, self.width // 2 + 50, self.height // 2 - card_height // 2)
        
        # Draw players' hands
        self.draw_players()
        
        # Draw animation if active
        if self.animation_active:
            # Calculate current position
            x = self.animation_start_pos[0] + (self.animation_end_pos[0] - self.animation_start_pos[0]) * self.animation_progress
            y = self.animation_start_pos[1] + (self.animation_end_pos[1] - self.animation_start_pos[1]) * self.animation_progress
            
            # Draw the card
            self.animation_card.draw(self.screen, int(x), int(y))
        
        # Draw color selection UI if needed
        if self.color_selection and self.current_player == 0:
            self.draw_color_selection()
        
        # Draw current player indicator
        current_player_text = self.font.render(f"Current Player: {self.players[self.current_player].name}", True, WHITE)
        self.screen.blit(current_player_text, (20, 20))
        
        # Draw direction indicator
        direction_text = "Direction: " + ("Clockwise" if self.direction == 1 else "Counter-Clockwise")
        direction_surface = self.font.render(direction_text, True, WHITE)
        self.screen.blit(direction_surface, (20, 50))
        
        # Draw game over message if game is over
        if self.game_over:
            self.draw_game_over()
        
        # Update the display
        pygame.display.flip()
    
    def draw_players(self):
        # Draw the human player's hand at the bottom
        human_player = self.players[0]
        card_spacing = 30
        hand_x = self.width // 2 - (len(human_player.hand) * card_spacing) // 2
        hand_y = self.height - 150 - 20
        
        human_player.draw_hand(self.screen, hand_x, hand_y, self.selected_card, True)
        
        # Draw AI players' hands
        num_ai_players = len(self.players) - 1
        
        if num_ai_players >= 1:  # Top player
            top_player = self.players[2] if num_ai_players >= 2 else self.players[1]
            top_x = self.width // 2 - (len(top_player.hand) * card_spacing) // 2
            top_y = 20
            top_player.draw_hand(self.screen, top_x, top_y, -1, False)
        
        if num_ai_players >= 2:  # Left player
            left_player = self.players[1]
            left_x = 20
            left_y = self.height // 2 - 75
            left_player.draw_hand(self.screen, left_x, left_y, -1, False)
        
        if num_ai_players >= 3:  # Right player
            right_player = self.players[3]
            right_x = self.width - 130
            right_y = self.height // 2 - 75
            right_player.draw_hand(self.screen, right_x, right_y, -1, False)
    
    def draw_color_selection(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw the prompt
        prompt_text = self.large_font.render("Choose a color:", True, WHITE)
        prompt_rect = prompt_text.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(prompt_text, prompt_rect)
        
        # Draw color buttons
        button_width = 100
        button_height = 50
        button_y = self.height // 2
        
        # Red button
        pygame.draw.rect(self.screen, RED, (self.width // 2 - 220, button_y, button_width, button_height))
        red_text = self.font.render("Red", True, WHITE)
        self.screen.blit(red_text, (self.width // 2 - 220 + 30, button_y + 15))
        
        # Blue button
        pygame.draw.rect(self.screen, BLUE, (self.width // 2 - 110, button_y, button_width, button_height))
        blue_text = self.font.render("Blue", True, WHITE)
        self.screen.blit(blue_text, (self.width // 2 - 110 + 30, button_y + 15))
        
        # Green button
        pygame.draw.rect(self.screen, GREEN, (self.width // 2 + 10, button_y, button_width, button_height))
        green_text = self.font.render("Green", True, BLACK)
        self.screen.blit(green_text, (self.width // 2 + 10 + 25, button_y + 15))
        
        # Yellow button
        pygame.draw.rect(self.screen, YELLOW, (self.width // 2 + 120, button_y, button_width, button_height))
        yellow_text = self.font.render("Yellow", True, BLACK)
        self.screen.blit(yellow_text, (self.width // 2 + 120 + 20, button_y + 15))
    
    def draw_game_over(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 192))
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over message
        game_over_text = self.large_font.render("Game Over!", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Draw winner message
        winner_text = self.large_font.render(f"{self.winner.name} wins!", True, WHITE)
        winner_rect = winner_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(winner_text, winner_rect)
        
        # Draw restart message
        restart_text = self.font.render("Press R to restart or Q to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        # Set up the game
        self.setup_game()
        
        # Game loop
        clock = pygame.time.Clock()
        
        while True:
            # Handle events
            self.handle_events()
            
            # Update animation
            self.update_animation()
            
            # AI turn
            if not self.game_over:
                self.ai_turn()
            
            # Draw the game
            self.draw_game()
            
            # Handle game over state
            if self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            # Restart the game
                            self.__init__()
                            self.setup_game()
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
            
            # Cap the frame rate
            clock.tick(60)
