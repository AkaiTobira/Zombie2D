import pygame


from obstacle  import Obstacle as Ob 
from vector    import Vector 
from physic    import UnitManager
from generator import ObjectsGenerator, Sandbox
from colors    import Colors, get_color

NUMBER_OF_ENEMIES   = 30
NUMBER_OF_OBSTACLES = 20

START_POSITION      = Vector(512,360)

class Game:
	screen      = None
	generator   = None
	unitManager = None
	running     = True 
	player      = None
	HUD			= None
	
	delta_time_ticks      = 0.0
	delta_time_seconds    = 0.0
	
	obj_on_screen = []
	
	def __init_screen_objects(self,resolution):
		self.obj_on_screen = self.generator.create_objects()
		self.player        = self.generator.get_spawned_player(START_POSITION, 100)
		self.unitManager   = UnitManager(self.obj_on_screen,self.player, self.screen, resolution)
	
	def __init_pygame(self, resolution,name):
		pygame.init()
		pygame.mouse.set_visible(False)
		pygame.display.set_caption(name)
		self.screen = pygame.display.set_mode(resolution)
		#delta_time = pygame.time.get_ticks()
	
	def __init__(self, resolution, name):
		self.__init_pygame(resolution,name)
		self.running  = True
		self.generator     = ObjectsGenerator(self.screen, NUMBER_OF_ENEMIES, NUMBER_OF_OBSTACLES,Vector(resolution[0],resolution[1]))
		self.__init_screen_objects(resolution)
		self.HUD = HUD(self.screen, self.player)		

	def is_running(self):
		return self.running
	
	def draw(self):
		self.unitManager.draw()
		self.HUD.draw() 
		pygame.display.flip()
		
	def process_input(self):
		while True:
			event = pygame.event.poll()
			if event.type == pygame.NOEVENT:
				return
			if event.type == pygame.QUIT:
				self.running = False
				return
			self.unitManager.process_input(event)
			
		
	def __calculate_delta_time(self):
		delta = pygame.time.get_ticks() - self.delta_time_ticks
		self.delta_time_ticks = delta
		self.delta_time_seconds = delta/100000.0
		
		
	def process_physic(self):
		self.__calculate_delta_time()
		self.unitManager.process_physic(self.delta_time_seconds)


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
		self.font = pygame.font.SysFont("consolas", self.font_size)
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