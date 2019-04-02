import pygame 
import game_functions as gf
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	# Initialize pygame, settings, and screen object.
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Battle for the Rebellion!")

	# Make the Play button.
	play_button = Button(ai_settings, screen, "Play")

	# Create an instance to store game statistics and create a scoreboard.
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)

	# Make a ship, a group of bullets, and a group of tie fighters.
	ship = Ship(ai_settings, screen)
	bullets = Group()
	tie_fs = Group()

	# Create the fleet of tie fighters.
	gf.create_fleet(ai_settings, screen, ship, tie_fs)


	# Start the main loop for the game.
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, 
			tie_fs, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, 
				tie_fs ,bullets)
			gf.update_tie_fs(ai_settings, screen, stats, sb, ship, tie_fs, 
				bullets)
		
		gf.update_screen(ai_settings, screen, stats, sb, ship, tie_fs, bullets, 
			play_button)

run_game()