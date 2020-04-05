import pygame as pg
import palette
from hitbox import *
from bound  import *


# define constants
BAR_LENGTH = 150
BAR_HEIGHT = 10
BAR_COLOR  = palette.DARK
BAR_SPEED  = 5


class Bar:

	def __init__(self, x, y, color=BAR_COLOR):
		# position
		self.x = x
		self.y = y

		# appearance
		self.width  = BAR_LENGTH
		self.height = BAR_HEIGHT
		self.color  = color

		# properties
		self.speed  = BAR_SPEED

		# hitbox & bound
		self.hitbox = Hitbox(self, [self.width, self.height])
		self.bound  = Bound (self, [1, 799], [545, 555])

	def render(self, screen):
		x = self.x - self.width //2
		y = self.y - self.height//2
		pg.draw.rect(screen, self.color, [x, y, self.width, self.height])
		if self.bound.show: self.bound.render(screen)
		if self.hitbox.show: self.hitbox.render(screen)
		if hasattr(self, 'trail'): self.trail.render(screen)

	def move(self, x=0, y=0):
		self.x += x
		self.y += y
		self.check_bounds()

	def check_bounds(self):
		if self.bound.check_left() : self.x = self.bound._left
		if self.bound.check_right(): self.x = self.bound._right

