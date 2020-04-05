import pygame as pg
import math
import palette
from hitbox import *
from bound  import *


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

		# hitbox & bound
		self.hitbox = Hitbox(self, [self.width, self.height])
		self.bound  = Bound (self, [300, 500], [200, 360])
		# self.bound.show = True

	def render(self, screen):
		pg.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.radius)
		if self.hitbox.show: self.hitbox.render(screen)
		if hasattr(self, 'trail'): self.trail.render(screen)
		if self.bound.show: self.bound.render(screen)

	def move(self):
		theta = math.radians(self.direction)
		self.x += math.sin(theta) * self.speed
		self.y += math.cos(theta) * self.speed
		self.check_bounds()

	def check_bounds(self):
		if self.bound.check_left():
			self.x = self.bound._left
			self.direction *= -1
		if self.bound.check_right():
			self.x = self.bound._right
			self.direction *= -1
		if self.bound.check_top():
			self.y = self.bound._top
			self.direction = 180 - self.direction
		if self.bound.check_bottom():
			self.y = self.bound._bottom
			self.direction = 180 - self.direction

	def release(self):
		self.bound  = Bound (self, [0, 800], [0, 640])

