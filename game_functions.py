import sys
import pygame
from bullet import Bullet
from tie_f import Tie_f
from time import sleep
from button import Button

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Respond to keypresses"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit not reached yet"""
	# Create a new bullet and add it to the bullets group.
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, tie_fs,
		bullets):
	"""Respond to keypresses and mouse events."""
	# Watch for keyboard and mouse events.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
				tie_fs, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, tie_fs, 
	bullets, mouse_x, mouse_y):
	"""Start a new game when the player clicks Play."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# Reset the game settings.
		ai_settings.initialize_dynamic_settings()

		# Hide the mouse cursor.
		pygame.mouse.set_visible(False)

		# Reset the game statistics.
		stats.reset_stats()
		stats.game_active = True

		# Reset the scoreboard images.
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_score()
		sb.prep_level()
		sb.prep_ships()

		# Empty the list of tie fighters and bullets.
		tie_fs.empty()
		bullets.empty()

		# Create a new fleet and center the ship.
		create_fleet(ai_settings, screen, ship, tie_fs)
		ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, tie_fs, bullets, 
		play_button):
	"""Update images on the screen and flip to the new screen."""
	# Redraw the screen during each pass through the loop.
	screen.fill(ai_settings.bg_color)

	# Redraw all bullets behind ship and tie fighters.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	tie_fs.draw(screen)

	# Draw the score information.
	sb.show_score()

	# Draw the play button if the is inactive.
	if not stats.game_active:
		play_button.draw_button()

	# Make the most recently drawn screen visible.
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, tie_fs, bullets):
	"""Update the position of bullets and get rid of old bullets."""
	# Update bullet positions.
	bullets.update()

	# Get rid of bullets that have disappeared. 
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_tie_f_collisions(ai_settings, screen, stats, sb, ship, 
		tie_fs, bullets)

def check_bullet_tie_f_collisions(ai_settings, screen, stats, sb,
		ship, tie_fs, bullets):
	"""Respond to bullet-tie fighter collisions."""
	# Remove any bullets and tie fighters that have collided. 
	collisions = pygame.sprite.groupcollide(bullets, tie_fs, True, True)
	if collisions:
		for tie_fs in collisions.values():
			stats.score += ai_settings.tie_f_points * len(tie_fs)
			sb.prep_score()
		check_high_score(stats, sb)

	if len(tie_fs) == 0:
		# If the entire fleet is destroyed, start a new level.
		bullets.empty()
		ai_settings.increase_speed()

		# Increases level.
		stats.level += 1
		sb.prep_level()

		create_fleet(ai_settings, screen, ship, tie_fs)

def get_num_tie_fs_x(ai_settings, tie_f_width):
	"""Determine the number of tie fighters that fit in a row."""
	available_space_x = ai_settings.screen_width - 2 * tie_f_width
	number_tie_f_x = int(available_space_x / (2 * tie_f_width))
	return number_tie_f_x

def get_num_rows(ai_settings, ship_height, tie_f_height):
	"""Determine the number of rows of tie fighters that fit on the screen."""
	available_space_y = (ai_settings.screen_height - (3 * tie_f_height) -
		ship_height)
	number_rows = int(available_space_y / (2 * tie_f_height))
	return number_rows

def create_tie_f(ai_settings, screen, tie_fs, tie_f_num, row_num):
	"""Create a tie fighter and place it in a row"""
	tie_f = Tie_f(ai_settings, screen)
	tie_f_width = tie_f.rect.width
	tie_f.x = tie_f_width + 2 * tie_f_width * tie_f_num
	tie_f.rect.x = tie_f.x
	tie_f.rect.y = tie_f.rect.height + 2 * tie_f.rect.height * row_num
	tie_fs.add(tie_f)


def create_fleet(ai_settings, screen, ship, tie_fs):
	"""Create a fleet full of tie fighters."""
	# Create a tie fighter and find the number of tie fighters in a row.
	tie_f = Tie_f(ai_settings, screen)
	tie_f_width = tie_f.rect.width
	number_tie_fs_x = get_num_tie_fs_x(ai_settings, tie_f_width)
	number_rows = get_num_rows(ai_settings, ship.rect.height, tie_f.rect.height)

	# Create the fleet of tie fighters.
	for row_num in range(number_rows):
		for tie_f_num in range(number_tie_fs_x):
			create_tie_f(ai_settings, screen, tie_fs, tie_f_num, row_num)

def check_fleet_edges(ai_settings, tie_fs):
	"""Respond appropriately if any tie fighters have reached an edge."""
	for tie_f in tie_fs.sprites():
		if tie_f.check_edges():
			change_fleet_direction(ai_settings, tie_fs)
			break

def change_fleet_direction(ai_settings, tie_fs):
	"""Drop the entire fleet and change the fleet's direction."""
	for tie_f in tie_fs.sprites():
		tie_f.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, tie_fs, bullets):
	"""Respond to ship being hit by tie fighter."""
	if stats.ships_left > 0:
		# Decrement ships left.
		stats.ships_left -= 1

		# Update scoreboard.
		sb.prep_ships()

		# Empty the list of tie fighters and bullets.
		tie_fs.empty()
		bullets.empty()

		# Create a new fleet and center the ship.
		create_fleet(ai_settings, screen, ship, tie_fs)
		ship.center_ship()

		# Pause.
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_bottom(ai_settings, screen, stats, sb, ship, tie_fs, bullets):
	"""Check if any aliens have reached the bottom of the screen."""
	screen_rect = screen.get_rect()
	for tie_f in tie_fs.sprites():
		if tie_f.rect.bottom >= screen_rect.bottom:
			# Treat this the same as if a ship was hit.
			ship_hit(ai_settings, screen, stats, sb, ship, tie_fs, 
				bullets)
			break


def update_tie_fs(ai_settings, screen, stats, sb, ship, tie_fs, bullets):
	"""
	Check if the fleet is at an edge, and then update the positions of all
	tie fighters in the fleet.
	"""
	check_fleet_edges(ai_settings, tie_fs)
	tie_fs.update()

	# Look for tie fighter / ship collisions.
	if pygame.sprite.spritecollideany(ship, tie_fs):
		ship_hit(ai_settings, screen, stats, sb, ship, tie_fs, bullets)
	# Look for tie fighters hitting the bottom of the screen.
	check_bottom(ai_settings, screen, stats, sb, ship, tie_fs, bullets)

def check_high_score(stats, sb):
	"""Check to see if there's a new high score."""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()