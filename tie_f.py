import pygame
from pygame.sprite import Sprite

class Tie_f(Sprite):
	"""A class to represent a single tie fighter in the fleet."""

	def __init__(self, ai_settings, screen):
		"""Initialize the tie fighter and set its starting position."""
		super(Tie_f,self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# Load the alien image and set its rect attribute.
		self.image = pygame.image.load_basic(
			'images/tie_f.bmp')
		self.rect = self.image.get_rect()

		# Start each new alien near the top left of the screen.
		self.rect.x = 25
		self.rect.y = 25

		# Store the alien's exact position.
		self.x = float(self.rect.x)

	def blitme(self):
		"""Draw the tie fighter at its current location."""
		self.screen.blit(self.image, self.rect)

	def check_edges(self):
		"""Return True if tie fighter is at edge of screen."""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True

	def update(self):
		"""Move the tie fighter right or left."""
		self.x += (self.ai_settings.tie_f_speed_fac * 
			self.ai_settings.fleet_direction)
		self.rect.x = self.x