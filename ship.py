import pygame

class Ship:
    """A class to manage the ship"""

    def __init__(self, ss_game):
        """Initialize the ship and set its starting position"""
        self.screen = ss_game.screen
        self.screen_rect = ss_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the midleft of the screen
        self.rect.midleft = self.screen.midleft

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)