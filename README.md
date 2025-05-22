# UNO Game

A high-quality graphical implementation of the classic UNO card game using Python and Pygame.

## Features

- Beautiful card graphics with smooth animations
- Play against up to 3 AI opponents
- Full implementation of UNO rules including:
  - Number cards (0-9)
  - Action cards (Skip, Reverse, Draw 2)
  - Wild cards (Wild, Wild Draw 4)
- Sound effects for card plays, draws, and game events
- Intuitive user interface

## Requirements

- Python 3.6 or higher
- Pygame 2.0 or higher

## Installation

1. Make sure you have Python installed
2. Install Pygame if you don't have it already:
   ```
   pip install pygame
   ```
3. Clone or download this repository

## How to Play

1. Navigate to the game directory
2. Run the game:
   ```
   python src/main.py
   ```

## Game Controls

- **Mouse**: Click on cards to select and play them
- **Number Keys (1-9)**: Select cards in your hand
- **Enter**: Play the selected card
- **D**: Draw a card from the deck
- **R**: Restart the game (after game over)
- **Q**: Quit the game (after game over)

## Game Rules

- Each player starts with 7 cards
- Players take turns matching a card in their hand with the card on the top of the discard pile
- Cards can be matched by color, number, or action
- If a player cannot match a card, they must draw a card from the draw pile
- Action cards:
  - **Skip**: The next player loses their turn
  - **Reverse**: The order of play is reversed
  - **Draw 2**: The next player must draw 2 cards and lose their turn
  - **Wild**: The player can choose any color
  - **Wild Draw 4**: The next player must draw 4 cards, lose their turn, and the player can choose any color
- The first player to get rid of all their cards wins

## Project Structure

- `src/main.py`: Entry point for the game
- `src/game.py`: Main game logic and rendering
- `src/deck.py`: Card deck management
- `src/card.py`: Card class definition
- `src/player.py`: Player class definition
- `assets/`: Directory for card images and sound effects

## Credits

Created by [Your Name]

## License

This project is licensed under the MIT License - see the LICENSE file for details.
