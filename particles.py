import pygame as pg
import math
import random
import palette
import collision
from hitbox import *


# define constants
RAINBOW_CYCLE_SPEED = 10
SCREEN_COLOR  = palette.SOFT_RED
# particles
PARTICLE_SPEED = 4
PARTICLE_SIZE  = 4
FADE_SPEED     = 0.95
# trail
NUM_PARTICLES  = 20


class Particle:
	'''a single particle'''
	def __init__(self, master, game, speed=PARTICLE_SPEED, direction=0, origin='plank',
	          size=PARTICLE_SIZE, shape='square', fade=FADE_SPEED, trail=None):
		self.master = master
		self.game   = game
		self.hitbox = Hitbox(self, size, size)

		# position
		self.x = self.master.x
		self.y = self.master.y

		# properties
		self.speed      = speed
		self.direction  = direction
		self.direction += master.direction + 180 if hasattr(master, 'direction') else 0
		self.bounce_spread = 70
		self.fade_speed = fade

		# appearance
		self.color = self.master.color if hasattr(master, 'color') else palette.DARK
		self.size  = size
		self.shape = shape
		self.trail = trail


		if origin == 'plank':
			offset = random.randint(-self.master.width//2,
			                         self.master.width//2)
			self.x = self.master.x + offset
			self.y = self.master.y + self.master.height//2

	def update(self):
		self.move()
		self.fade()

	def render(self, screen):
		# if self.hitbox.show: self.hitbox.render(screen)
		if self.shape == 'square':
			pg.draw.rect(screen, self.color, [self.x-self.size//2, self.y-self.size//2, self.size, self.size])
			return
		if self.shape == 'circle':
			pg.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.size//2)
			return

	def fade(self, fade_speed=FADE_SPEED):
		self.color = self.blendColor(self.color, self.game.screen_color, self.fade_speed)

	def blendColor(self, color0, color1, ratio=0.5):
		return [color0[idx]*ratio + color1[idx]*(1-ratio) for idx in range(3)]

	def move(self):
		theta = math.radians(self.direction)
		self.x += math.sin(theta) * self.speed
		self.y += math.cos(theta) * self.speed
		
		self.check_bounds()
		self.check_collision()

	def check_bounds(self):
		if self.x <= 0:
			x = 0
			self.direction = -90
			self.bounce()
		if self.x >= 800:
			x = 800
			self.direction = 90
			self.bounce()
		if self.y <= 0:
			y = 0
			self.direction = 180 - self.direction
			self.bounce()
		if self.y >= 640:
			y = 640
			self.direction = 180 - self.direction
			self.bounce()

	def check_collision(self):
		if collision.detect(self.game.bar, self):
			self.direction = 180 - self.direction
			self.bounce()

	def bounce(self):
		self.direction += random.randint(-self.bounce_spread, self.bounce_spread)




class Trail:
	'''a trail of particles'''
	def __init__(self, master, game, density=1, spread=0, fade=FADE_SPEED,
					ptcl_speed=PARTICLE_SPEED, direction=0, origin='plank',
					ptcl_size=PARTICLE_SIZE, ptcl_shape='square', style=None):
		self.master = master
		self.game   = game

		# properties
		self.density   = density
		self.spread    = spread
		self.direction = direction
		self.fade      = fade
		self.origin    = origin
		self.style     = None

		# variables
		self.idx = 0
		self.qty = NUM_PARTICLES * self.density

		# particle properties
		self.fade_speed = FADE_SPEED
		self.ptcl_speed = ptcl_speed
		self.ptcl_size  = ptcl_size
		self.ptcl_shape = ptcl_shape

		# trail
		self.trail = [self.place_ptcl()] * self.qty

	def place_ptcl(self):
		return Particle(self.master, self.game, speed=self.ptcl_speed, fade=self.fade,
				direction=random.randint(-self.spread, self.spread) + self.direction,
				origin=self.origin, trail=self,
				size=self.ptcl_size, shape=self.ptcl_shape)

	def update(self):
		for ptcl in self.trail: ptcl.update()
		self.qty = NUM_PARTICLES * self.density
		self.idx = (self.idx+self.density) % self.qty
		for itr in range(self.density):
			self.trail[(self.idx+itr) % self.qty] = self.place_ptcl()

	def render(self, screen):
		for ptcl in self.trail: ptcl.render(screen)





def make(master, game, density=1, spread=0, fade=FADE_SPEED,
				ptcl_speed=PARTICLE_SPEED, direction=0, origin='plank',
				ptcl_size=PARTICLE_SIZE, ptcl_shape='square', style=None):
	master.trail = Trail(master, game, density, spread, fade,
							ptcl_speed, direction, origin,
							ptcl_size, ptcl_shape, style)

def remove(master):
	try:
		del master.trail
	except:
		pass


