import json

class GameStats:
    """Track stats for Sideways Shooter"""

    def __init__(self, ss_game):
        """Initialize statistics"""
        self.settings = ss_game.settings
        self.reset_stats()

        # Start Sideways Shooter in an inactive state
        self.game_active = False

        # High score should never be reset
        try:
                filename = 'high_score.json'
                with open(filename) as f:
                    self.high_score = json.load(f)     
        except json.decoder.JSONDecodeError:
            self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1