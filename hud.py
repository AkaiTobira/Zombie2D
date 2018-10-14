import pygame

from colors    import Colors, get_color

class HUD:

	color 		 	= get_color(Colors.WHITE)
	font_size 	 	= 20
	font 		 	= None
	screen 		 	= None
	player		 	= None

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

	def HP(self):
		return max(0, self.player.get_HP())	

	def render_text(self, text):
		return self.font.render( str(text), True, self.color )	

	def draw_HP(self):
		self.screen.blit(self.render_text("HP : " + str(self.HP()) + " / " + str(self.HP_max)), self.hp_txt_position)

	def draw_HP_bar(self):
		pygame.draw.rect(self.screen, self.hp_bar_color, (self.hp_bar_position[0], self.hp_bar_position[1], self.HP() * self.bar_width / self.HP_max, 10))
		pygame.draw.rect(self.screen, self.hp_bar_color, (self.hp_bar_position[0], self.hp_bar_position[1], self.bar_width, 10), 1)

	def draw(self):
		self.draw_HP()
		self.draw_HP_bar()