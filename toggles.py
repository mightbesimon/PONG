import pygame as pg
import particles as trail
from hitbox import *
from bound  import *


class Action:
	 def __init__(self, key, function):
	 	self.key     = key
	 	self.execute = function


class Toggle:

	def __init__(self, master):
		self.game = master

	def cheats (self): self.game.cheats  = not self.game.cheats
	def paused (self): self.game.paused  = not self.game.paused
	def showfps(self): self.game.showfps = not self.game.showfps
	def showHitbox(self):    Hitbox.show = not Hitbox.show
	def showBounds(self):    Bound.show  = not Bound.show

	def particles(self):
		if hasattr(self.game.bar,  'trail'):
			trail.remove(self.game.bar )
		else:
			trail.make(self.game.bar,  self.game, density=10, spread=30)
			self.game.bar.trail.density = 4
		trail.remove(self.game.ball) if hasattr(self.game.ball, 'trail') else trail.make(self.game.ball, self.game, density=2,  spread=10, fade=0.88, ptcl_speed=4-self.game.ball.speed, origin='point')



def make(master):
	toggle = Toggle(master)

	cheats     = Action(key=pg.K_c, function=toggle.cheats    )
	paused     = Action(key=pg.K_p, function=toggle.paused    )
	showfps    = Action(key=pg.K_f, function=toggle.showfps   )
	showHitbox = Action(key=pg.K_h, function=toggle.showHitbox)
	showBounds = Action(key=pg.K_b, function=toggle.showBounds)
	particles  = Action(key=pg.K_t, function=toggle.particles )


	return [
		cheats,
		paused,
		showfps,
		showHitbox,
		showBounds,
		particles,
	]

def check(toggles, event):
	if event.type != pg.KEYDOWN: return
	for action in toggles:
		if event.key == action.key:
			action.execute()

