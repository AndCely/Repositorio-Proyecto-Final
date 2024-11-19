import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.setting = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        self.setting.screen_width = self.screen.get_rect().width
        self.setting.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")


        # Create an instance to store game statistics.
        self.stats = GameStats(self) 
        # Create an instance to store game statistics, and create a scoreboard.
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Make the Play button.
        self.play_button = Button(self, "Play")



        # Set the background color.
        self.bg_color = (35, 35, 35)
    def run_game(self):
       while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

            
         
            

    def _check_events(self):
        """Respond to keypresses and mouse events.""" 
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  
                
                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)

                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                     mouse_pos = pygame.mouse.get_pos()
                     self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
         "Start a new game when the player clicks Play"
         button_clicked = self.play_button.rect.collidepoint(mouse_pos)
         if button_clicked and not self.stats.game_active:
              
              # Reset the game settings.
              self.setting.initialize_dynamic_settings()
              # Reset the game statistics.
              self.stats.reset_stats()
              self.stats.game_active = True
              self.sb.prep_score()
              self.sb.prep_level()
              self.sb.prep_ships()

              # Get rid of any remaining aliens and bullets.
              self.aliens.empty()
              self.bullets.empty()

              # Create a new fleet and center the ship.
              self._create_fleet()
              self.ship.center_ship()

              # Hide the mouse cursor.
              pygame.mouse.set_visible(False)
                    
    def _check_keydown_events(self,event):
         """Respond to keypresses."""
         if event.key == pygame.K_RIGHT:
              # Move the ship to the right.
              self.ship.moving_right = True
         elif event.key == pygame.K_LEFT:
              self.ship.moving_left = True
         elif event.key == pygame.K_q:
              sys.exit()
         elif event.key == pygame.K_SPACE:
              self._fire_bullet()   

    def _check_keyup_events(self, event):
         """Respond to releases."""
         if event.key == pygame.K_RIGHT:
               self.ship.moving_right = False
         elif event.key == pygame.K_LEFT:
               self.ship.moving_left = False
     
    def _fire_bullet(self):
         """Create a new bullet and add it ti the bullets group"""
         if len(self.bullets) < self.setting.bullets_allowed:  
          new_bullet = Bullet(self)
          self.bullets.add(new_bullet)
         

    def _update_screen(self):
            """Update images on the screen, and flip to the new screen.""" 
            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.setting.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
               bullet.draw_bullet()
              
            # Draw the score information.
            self.sb.show_score()

            # Draw the play button if the game is inactive.
            if not self.stats.game_active:
                self.play_button.draw_button()

            # Make the most recently drawn screen visible.
            pygame.display.flip()
            
    def _update_bullets(self):
         """Update position of bullets and get rid of old bullets."""
          # Update bullet positions.
         self.bullets.update()
            
            # Get rid of bullets that have disappeared.
         for bullet in self.bullets.copy():
               if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
               print(len(self.bullets))

    def _ship_hit(self):
          """Respond to ship being hit by alien."""
          if self.stats.ships_left > 0:
               # Decrement ships_left, and update scoreboard.
               self.stats.ships_left -= 1
               self.sb.prep_ships()
          else:
               self.stats.game_active = False
               pygame.mouse.set_visible(True)

    def _check_bullet_alien_collisions(self):
          """Respond to bullet-alien collisions."""
          # Remove any bullets and aliens that have collided.
          collisions = pygame.sprite.groupcollide(
          self.bullets, self.aliens, True, True)

          if collisions:
               for aliens in collisions.values():
                    self.stats.score += self.setting.alien_points * len(aliens)
               self.sb.prep_score()
               self.sb.check_high_score()

          if not self.aliens:
               # Destroy existing bullets and create new fleet.
               self.bullets.empty()
               self._create_fleet()
               self.setting.increase_speed()

               # Increase level.
               self.stats.level += 1
               self.sb.prep_level()

            


if __name__ == '__main__':
 # Make a game instance, and run the game.
 ai = AlienInvasion()
 ai.run_game()