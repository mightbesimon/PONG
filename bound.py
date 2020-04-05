import pygame as pg

ORANGE = [255, 172,  32]


class Bound():
	"""bound attribute of game objects"""
	show = False

	def __init__(self, master, horizontal, vertical, color=ORANGE):
		self.master = master
		self.left, self.right  = horizontal
		self.top,  self.bottom = vertical
		self._left   = self.left   + self.master.hitbox.width //2
		self._right  = self.right  - self.master.hitbox.width //2
		self._top    = self.top    + self.master.hitbox.height//2
		self._bottom = self.bottom - self.master.hitbox.height//2

		self.color  = color

	def render(self, screen):
		pg.draw.rect(screen, self.color, [self.left, self.top, self.right-self.left, self.bottom-self.top], 2)

	def check_left(self):
		return self.master.x < self._left

	def check_right(self):
		return self.master.x > self._right

	def check_top(self):
		return self.master.y < self._top

	def check_bottom(self):
		return self.master.y > self._bottom

