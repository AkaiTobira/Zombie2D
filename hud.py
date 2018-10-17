import pygame

from vector 	import Vector
from colors    	import Colors, get_color

class Cursor:

	COLOR       = get_color(Colors.YELLOW)	
	RADIUS	    = 12	
	THICK	    = 1	
	position 	= Vector(0,0)
	screen      = None

	def __init__(self, screen):
		self.screen = screen

	def process_event(self, event):
		if event.type == pygame.MOUSEMOTION:
			self.position = (Vector(event.pos[0], event.pos[1]))

	def draw(self):
		pygame.draw.circle(self.screen, self.COLOR, self.position.to_table(), self.RADIUS, self.THICK)
		pygame.draw.line(self.screen, self.COLOR, Vector(self.position.x-self.RADIUS, self.position.y).to_table(), Vector(self.position.x+self.RADIUS,self.position.y).to_table(), self.THICK)
		pygame.draw.line(self.screen, self.COLOR, Vector(self.position.x, self.position.y-self.RADIUS).to_table(), Vector(self.position.x, self.position.y+self.RADIUS).to_table(), self.THICK)


class HUD:

	color 		 	= get_color(Colors.WHITE)
	font_size 	 	= 20
	font 		 	= None
	screen 		 	= None
	player		 	= None
	cursor			= None

	HP_max		 	= 0
	hp_bar_color 	= get_color(Colors.LIGHT_RED)
	hp_txt_position = (30,30)
	hp_bar_position = (30,60)

	delta 			= 0
	cooldown        = 100 
	cd_bar_color 	= get_color(Colors.BLUE_BAR)
	cd_txt_position = (780,30)
	cd_bar_position = (840,60)
	
	bar_width	 	= 150


	def __init__(self, screen, player):
		self.screen = screen
		self.font   = pygame.font.SysFont("consolas", self.font_size)
		self.player = player
		self.HP_max = player.get_HP()
		self.cursor = Cursor(screen)
		self.delta  = self.cooldown

	def HP(self):
		return max(0, self.player.get_HP())	

	def render_text(self, text):
		return self.font.render( str(text), True, self.color )

	def calculate_cooldown(self):
		if self.delta >= 1: 
			self.delta -= 0.1
		if self.delta == 0:
			self.delta = self.cooldown	

	def draw_HP_amount(self):
		self.calculate_cooldown()
		self.screen.blit(self.render_text("HP : " + str(self.HP()) + " / " + str(self.HP_max)), self.hp_txt_position)

	def draw_cooldown_amount(self):
		self.screen.blit(self.render_text("COOLDOWN : " + str(round(self.delta)) + " / " + str(self.cooldown)), self.cd_txt_position)	

	def draw_bar(self, color, position, fill):
		pygame.draw.rect(self.screen, color, (position[0], position[1], fill, 10))
		pygame.draw.rect(self.screen, color, (position[0], position[1], self.bar_width, 10), 1)	

	def draw_HP_bar(self):
		self.draw_bar (
			self.hp_bar_color, 
			self.hp_bar_position, 
			self.HP() * self.bar_width / self.HP_max )

	def draw_cooldown_bar(self):
		self.draw_bar (
			self.cd_bar_color, 
			self.cd_bar_position, 
			self.delta / 100 * self.bar_width )			

	def process_event(self, event):
		self.cursor.process_event(event)	

	def draw(self):
		self.cursor.draw()

		self.draw_HP_amount()
		self.draw_HP_bar()

		self.draw_cooldown_amount()
		self.draw_cooldown_bar()

