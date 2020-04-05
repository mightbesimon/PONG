import pygame as pg

GREEN = [ 32, 255,  32]


class Hitbox():
	"""hitbox attribute of game objects"""
	show = False

	def __init__(self, master, dimension, color=GREEN):
		self.master = master
		self.width, self.height = dimension

		self.color  = color

	def render(self, screen):
		x = self.master.x - self.width //2
		y = self.master.y - self.height//2
		pg.draw.rect(screen, self.color, [x, y, self.width, self.height], 2)

