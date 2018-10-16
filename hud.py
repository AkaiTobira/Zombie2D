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
	
	bar_width	 	= 150


	def __init__(self, screen, player):
		self.screen = screen
		self.font   = pygame.font.SysFont("consolas", self.font_size)
		self.player = player
		self.HP_max = player.get_HP()
		self.cursor = Cursor(screen)

	def HP(self):
		return max(0, self.player.get_HP())	

	def render_text(self, text):
		return self.font.render( str(text), True, self.color )	

	def draw_HP(self):
		self.screen.blit(self.render_text("HP : " + str(self.HP()) + " / " + str(self.HP_max)), self.hp_txt_position)

	def draw_HP_bar(self):
		pygame.draw.rect(self.screen, self.hp_bar_color, (self.hp_bar_position[0], self.hp_bar_position[1], self.HP() * self.bar_width / self.HP_max, 10))
		pygame.draw.rect(self.screen, self.hp_bar_color, (self.hp_bar_position[0], self.hp_bar_position[1], self.bar_width, 10), 1)

	def process_event(self, event):
		self.cursor.process_event(event)	

	def draw(self):
		self.cursor.draw()
		self.draw_HP()
		self.draw_HP_bar()