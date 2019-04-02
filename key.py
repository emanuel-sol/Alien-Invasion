import sys

import pygame

def run_game():
	# Initialize pygame, settings, and screen object.
	pygame.init()
	screen = pygame.display.set_mode((1200,700))
	pygame.display.set_caption("Key Test")

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				print(event.type)
		pygame.display.flip()

run_game()

