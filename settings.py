class Settings(object):
	"""A class to to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's static settings."""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 700
		self.bg_color = (135,206,250)

		# Ship settings
		self.ship_limit = 3

		# Bullet settings
		self.bullet_width = 5
		self.bullet_height = 25 
		self.bullet_color = 255,0,0
		self.bullets_allowed = 3

		# Tie fighter settings
		self.fleet_drop_speed = 10

		# How quickly the game speeds up
		self.speedup_scale = 1.1
		# How quickly the tie fighter point values increase
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game."""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.tie_f_speed_fac = 1
		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# Scoring 
		self.tie_f_points = 50

	def increase_speed(self):
		"""Increase speed settings and tie fighter point values"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.tie_f_speed_fac *= self.speedup_scale

		self.tie_f_points = int(self.tie_f_points * self.score_scale)