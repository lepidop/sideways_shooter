class Settings:
    """A class to store all the settings for Sideways Shooter"""

    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.bg_color = (0,0,0)
        
        # Ship settings
        self.ship_speed = 0.5

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 15
        self.bullet_height = 5
        self.bullet_color = (200,200,200)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 0.2
        self.alien_spawn_rate = 2000