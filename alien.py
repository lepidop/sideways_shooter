import pygame
from pygame.sprite import Sprite
from random import randint

class Alien(Sprite):
    """A class to manage aliens"""

    def __init__(self, ss_game):
        """
        Create an alien object at a random position 
        on the right side of the screen
        """
        super().__init__()
        self.screen = ss_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ss_game.settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each alien near the top left of the screen.
        self.rect.midright = self.screen_rect.midright
        self.rect.y = randint(0, 
                              self.settings.screen_height - self.rect.y)

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)
       
    def update(self):
        """Move the alien ship right or left"""
        self.x -= self.settings.alien_speed
        self.rect.x = self.x