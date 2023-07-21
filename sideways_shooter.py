import sys
from time import sleep
import json

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class SidewaysShooter:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # Create an instance to store game statistics, and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.play_button = Button(self, "Play")

        self.aliens = pygame.sprite.Group()

        self.CREATEALIEN = pygame.USEREVENT + 1
        pygame.time.set_timer(self.CREATEALIEN, self.settings.alien_spawn_rate)

        # Play music and prep sound effect
        pygame.mixer.music.load('sounds/background.wav')
        pygame.mixer.music.play()

        self.blaster_noise = pygame.mixer.Sound('sounds/attack.wav')
    
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_aliens()
                self._update_bullets()
            
            self._update_screen()

    def _check_events(self):
        # Respond to keypresses and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_program()
            elif event.type == self.CREATEALIEN and self.stats.game_active:  
                new_alien = Alien(self)
                self.aliens.add(new_alien)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _end_program(self):
        filename = 'high_score.json'
        with open(filename, 'w') as f:
            json.dump(self.stats.high_score, f)
        sys.exit()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings and statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Center the ship
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            self._end_program()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
                    self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.blaster_noise.play()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet position
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.settings.screen_width:
                self.bullets.remove(bullet)
            
        # Check for any bullets that have hit aliens
        #   If so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, 
                                                True, True)
        
        if collisions:
            self._progress_after_collision(collisions)
        
    def _progress_after_collision(self, collisions):
        for aliens in collisions.values():
            self.stats.score += self.settings.alien_points * len(aliens)
        self.sb.prep_score()
        self.sb.check_high_score()
        
        if self.settings.aliens_to_level_up > 0:
            self.settings.aliens_to_level_up -= 1
        else:
            self.settings.aliens_to_level_up = 9
            self._level_up()

    def _level_up(self):
        self.stats.level += 1
        self.sb.prep_level()
        self.settings.increase_speed()
                
    def _update_aliens(self):
        """Update position of aliens and get rid of old aliens"""
        # Update alien position
        self.aliens.update()

        # If an alien has reached the end of the screen,
        # respond as if the ship were hit
        for alien in self.aliens.copy():
            if alien.rect.right < 0:
                self._ship_hit()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement the ships left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bulletss
            self.aliens.empty()
            self.bullets.empty()

            # Center the ship
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self._game_over()

    def _game_over(self):
        self.stats.game_active = False
        pygame.mouse.set_visible(True)

    def _update_screen(self):
        # Update images on the screen, and flip to the new screen
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.ship.blitme()

        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ss = SidewaysShooter()
    ss.run_game()