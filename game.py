import pygame as pg
import palette
from bar  import *
from ball import *
import particles as trail
import toggles
import collision


# define constants #
#fps
FPS      = 30
SHOW_FPS = False

# screen
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 640
SCREEN_COLOR  = palette.SOFT_RED


class Game:

	def __init__(self, window_name='demo'):
		self.name = window_name

	def setup(self):
		pg.init()
		self.clock = pg.time.Clock()

		# initialise screen
		self.screen_color = SCREEN_COLOR
		self.screen = pg.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
		pg.display.set_caption(self.name)

		# font
		self.infofont  = pg.font.Font(None, 20)
		self.scorefont = pg.font.Font(None, 50)

		# settings
		self.fps = FPS

		# game states
		self.over 	 = False
		self.paused  = False
		self.cheats  = False
		self.menu    = 'start_menu'

		self.score   = 0

		# info
		self.showfps   = SHOW_FPS
		self.debugging = False

		# game objects
		self.bar  = Bar(400, 550)
		self.ball = Ball(400, 240)
		trail.make(self.bar,  self, life=30, density=10, spread=30)
		self.bar.trail.density = 4
		trail.make(self.ball, self, density=2,  spread=10, fade_speed=0.88,
		           ptcl_speed=4-self.ball.speed, origin='point')

		# helper containers
		self.toggles = toggles.make(self)

	def tick(self):
		self.getevent()
		self.update() if not self.paused else None
		self.getinfo()
		self.render()

	def cleanup(self):
		pg.quit()



# class tick:

	def getevent(self):
		for event in pg.event.get():
			if event.type == pg.QUIT: self.over = True

			if self.menu == 'start_menu':
				# if toggles.check(self.toggles, event, check_list=['showBounds']):
				if (event.type == pg.KEYUP
						and event.key == self.toggles['showBounds'].key):
					self.toggles['showBounds'].execute()
				elif (event.type == pg.KEYUP
						or event.type == pg.KEYDOWN
						and(event.key==pg.K_LEFT or event.key==pg.K_RIGHT)):
					self.menu = None
					self.ball.release()
				break


			toggles.check(self.toggles, event)

			if event.type == pg.KEYUP:
				# Q to quit game
				if event.key == pg.K_q:
					self.over = True


		# adjustments
		keys = pg.key.get_pressed()

		self.barMove = 0
		if keys[pg.K_LEFT]:
			self.barMove -= self.bar.speed
		if keys[pg.K_RIGHT]:
			self.barMove += self.bar.speed

	def update(self):
		# position
		if self.cheats: self.barMove = self.ball.x - self.bar.x
		self.bar.move(x=self.barMove)
		self.ball.move()

		# trails
		if hasattr(self.bar,  'trail'): self.bar.trail.update()
		if hasattr(self.ball, 'trail'): self.ball.trail.update()

		if collision.detect(self.bar, self.ball):
			self.ball.direction = 180 - self.ball.direction
			self.score += 1

	def getinfo(self):
		self.clock.tick(self.fps)
		self.fps_info   = self.infofont.render(f'FPS   = {self.clock.get_fps():.2f}', True, palette.SNOW)
		self.debug_info = self.infofont.render(f'debug info: {None}', True, palette.SNOW)

		self.score_info = self.scorefont.render(f'{self.score}', True, palette.SNOW)

		self.start_menu = []
		self.start_menu.append({'message' : make_message('PONG', palette.DARK, 80),
								'position': [400, 240]})
		self.start_menu.append({'message' : make_message('PRESS [any key] TO CONTINUE', palette.DARK),
								'position': [400, 300]})

		self.pause_menu = []
		self.pause_menu.append({'message' : self.scorefont.render('PAUSED', True, palette.DARK),
								'position': [400, 270]})
		self.pause_menu.append({'message' : self.infofont.render('PRESS [P] TO CONTINUE', True, palette.DARK),
								'position': [400, 320]})
		'''
		self.pause_menu.append({'message' : self.infofont.render('[P] toggle pause', True, palette.SNOW),
								'position': [309, 340]})
		self.pause_menu.append({'message' : self.infofont.render('[C] toggle cheats', True, palette.SNOW),
								'position': [309, 355]})
		self.pause_menu.append({'message' : self.infofont.render('[F] toggle show fps', True, palette.SNOW),
								'position': [309, 370]})
		self.pause_menu.append({'message' : self.infofont.render('[H] toggle show collision box', True, palette.SNOW),
								'position': [309, 385]})
		self.pause_menu.append({'message' : self.infofont.render('[T] toggle show particles', True, palette.SNOW),
								'position': [309, 400]})
		'''

	def render(self):
		# clear screen
		self.screen.fill((self.screen_color))

		# bar, ball
		self.bar.render(self.screen)
		self.ball.render(self.screen)

		# score
		if self.menu == None:
			self.screen.blit(self.score_info, [765-self.score_info.get_width(), 30])

		if self.menu == 'start_menu':
			for item in self.start_menu:
				self.screen.blit(item['message'], [400-item['message'].get_width()//2, item['position'][1]])

		if self.paused:
			for item in self.pause_menu[:2]:
				self.screen.blit(item['message'], [400-item['message'].get_width()//2, item['position'][1]])
			# for item in self.pause_menu[2:]:
			# 	self.screen.blit(item['message'], item['position'])

		# info
		if self.showfps:   self.screen.blit(self.fps_info,   [50, 50])
		if self.debugging: self.screen.blit(self.debug_info, [50, 66])

		pg.display.update()



def make_message(message, color, size=20):
	font = pg.font.Font(None, size)
	return font.render(message, True, color)


