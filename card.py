import pygame

# Card colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.width = 100
        self.height = 150
        self.image = None
        self.back_image = None
        self.face_up = True
        
    def load_images(self):
        # Load card images based on color and value
        try:
            image_path = f"../assets/cards/{self.color}_{self.value}.png"
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except:
            # Create a card image if file doesn't exist
            self.image = self.create_card_image()
            
        # Create card back
        self.back_image = self.create_card_back()
    
    def create_card_image(self):
        # Create a surface for the card
        card_surface = pygame.Surface((self.width, self.height))
        
        # Set background color based on card color
        if self.color == "red":
            bg_color = RED
        elif self.color == "blue":
            bg_color = BLUE
        elif self.color == "green":
            bg_color = GREEN
        elif self.color == "yellow":
            bg_color = YELLOW
        else:  # wild cards
            bg_color = BLACK
            
        # Fill the card with background color
        card_surface.fill(bg_color)
        
        # Draw a white rectangle for the card border
        pygame.draw.rect(card_surface, WHITE, (5, 5, self.width - 10, self.height - 10))
        
        # Draw a colored rectangle inside the white border
        pygame.draw.rect(card_surface, bg_color, (10, 10, self.width - 20, self.height - 20))
        
        # Add text for the card value
        font = pygame.font.SysFont('Arial', 40, bold=True)
        
        # Text color is white for dark backgrounds, black for light backgrounds
        text_color = WHITE if self.color in ["blue", "red", "green", "wild"] else BLACK
        
        # Render the text
        text = font.render(str(self.value), True, text_color)
        
        # Position the text in the center of the card
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        card_surface.blit(text, text_rect)
        
        # Add smaller text in corners
        small_font = pygame.font.SysFont('Arial', 20, bold=True)
        small_text = small_font.render(str(self.value), True, text_color)
        card_surface.blit(small_text, (10, 10))
        card_surface.blit(small_text, (self.width - 25, self.height - 25))
        
        return card_surface
    
    def create_card_back(self):
        # Create a surface for the card back
        back_surface = pygame.Surface((self.width, self.height))
        
        # Fill with dark blue
        back_surface.fill((0, 0, 100))
        
        # Draw a white border
        pygame.draw.rect(back_surface, WHITE, (5, 5, self.width - 10, self.height - 10), 2)
        
        # Draw the UNO logo
        font = pygame.font.SysFont('Arial', 40, bold=True)
        text = font.render("UNO", True, WHITE)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        back_surface.blit(text, text_rect)
        
        return back_surface
    
    def draw(self, surface, x, y):
        # Draw the card at the specified position
        if self.face_up:
            surface.blit(self.image, (x, y))
        else:
            surface.blit(self.back_image, (x, y))
    
    def flip(self):
        # Flip the card
        self.face_up = not self.face_up
    
    def __str__(self):
        return f"{self.color} {self.value}"
