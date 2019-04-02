class GameStats(object):
	"""Track statistics for 'Battle for the Rebellion!'"""

	def __init__(self, ai_settings):
		"""Initialize statistics."""
		self.ai_settings = ai_settings
		self.reset_stats()
		# Start game in an active state.
		self.game_active = True

		# Start game in an inactive state.
		self.game_active = False

		# High score should never be reset.
		self.high_score = 0
		self.level = 1

	def reset_stats(self):
		"""Iniatialize statistics that can change during the game."""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0