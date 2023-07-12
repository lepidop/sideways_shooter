class Settings:
    """A class to store all the settings for Sideways Shooter"""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen settings
        self.bg_color = (0,0,0)
        
        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 15
        self.bullet_height = 5
        self.bullet_color = (200,200,200)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_spawn_rate = 2000

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_increase = 10

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initalize settings that change throughout the game"""
        self.ship_speed = 0.5
        self.bullet_speed = 1.0
        self.alien_speed = 0.2
        self.aliens_to_level_up = 9

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_spawn_rate *= self.speedup_scale

        self.alien_points += self.score_increase