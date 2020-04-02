import pygame as pg
import math
import palette
from hitbox import *


# define constants
BALL_DIAMETER = 10
BALL_COLOR    = palette.SNOW
BALL_SPEED    = 8


class Ball:

	def __init__(self, x, y, color=BALL_COLOR):
		# position
		self.x = x
		self.y = y

		# appearance
		self.diameter = BALL_DIAMETER
		self.radius   = BALL_DIAMETER // 2
		self.width    = self.diameter
		self.height   = self.diameter
		self.color    = color

		# property
		self.speed     = BALL_SPEED
		self.direction = 160

		# hitbox
		self.hitbox = Hitbox(self, self.width, self.height)

	def render(self, screen):
		pg.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.radius)
		if self.hitbox.show: self.hitbox.render(screen)
		if hasattr(self, 'trail'): self.trail.render(screen)
		# if self.hasTrail: self.trail.render(direction=self.direction, spread=10, origin='point')
		


	def move(self):
		theta = math.radians(self.direction)
		self.x += math.sin(theta) * self.speed
		self.y += math.cos(theta) * self.speed
		self.check_bounds()

	def check_bounds(self):
		if self.x <= 0:
			x = 0
			self.direction *= -1
		if self.x >= 800:
			x = 800
			self.direction *= -1
		if self.y <= 0:
			y = 0
			self.direction = 180 - self.direction
		if self.y >= 640:
			y = 640
			self.direction = 180 - self.direction


