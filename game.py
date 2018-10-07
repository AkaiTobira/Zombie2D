import pygame


from obstacle  import Obstacle as Ob 
from physic    import *
from generator import *

NUMBER_OF_ENEMIES   = 25
NUMBER_OF_OBSTACLES = 10

START_POSITION      = [512,360]

class Game:
	screen      = None
	generator   = None
	unitManager = None
	running     = True 
	player      = None
	
	delta_time_ticks      = 0.0
	delta_time_seconds    = 0.0
	
	obj_on_screen = []
	
	def __init_screen_objects(self):
		self.obj_on_screen = self.generator.create_objects()
		self.player        = self.generator.get_spawned_player(START_POSITION)
		self.unitManager   = UnitManager(self.obj_on_screen,self.player, self.screen)
	
	def __init_pygame(self, resolution,name):
		pygame.init()
		pygame.display.set_caption(name)
		self.screen = pygame.display.set_mode(resolution)
		delta_time = pygame.time.get_ticks()
	
	def __init__(self, resolution, name):
		self.__init_pygame(resolution,name)
		self.running  = True
		self.generator     = ObjectsGenerator(self.screen, NUMBER_OF_ENEMIES, NUMBER_OF_OBSTACLES)
		self.__init_screen_objects()

	def is_running(self):
		return self.running
	
	def draw(self):
		self.unitManager.draw()
		
	def process_input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				return
			self.unitManager.process_input(event)
			
		
	def __calculate_delta_time(self):
		delta = pygame.time.get_ticks() - self.delta_time_ticks
		self.delta_time_ticks = delta
		self.delta_time_seconds = delta/1000.0
		
		
	def process_physic(self):
		self.__calculate_delta_time()
		self.unitManager.process_physic(self.delta_time_seconds)
