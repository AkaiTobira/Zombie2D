import pygame


from obstacle import Obstacle as Ob 
from generator import *

NUMBER_OF_ENEMIES   = 10
NUMBER_OF_OBSTACLES = 5

START_POSITION      = [512,360]

class Game:
	screen    = None
	generator = None
	running   = True 
	player    = None
	
	delta_time_ticks      = 0.0
	delta_time_seconds    = 0.0
	
	obj_on_screen = []
	
	def __init_screen_objects(self):
		self.obj_on_screen = self.generator.create_objects()
		self.player        = self.generator.get_spawned_player(START_POSITION)
	
	
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
		self.screen.fill((20,30,47))
		for obj in self.obj_on_screen:
			obj.draw()
		self.player.draw()
		pygame.display.flip()
		
	def process_input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				return
			for obj in self.obj_on_screen:
				obj.process_event(event)
			self.player.process_event(event)
		
	def __calculate_delta_time(self):
		delta = pygame.time.get_ticks() - self.delta_time_ticks
		self.delta_time_ticks = delta
		self.delta_time_seconds = delta/1000.0
		
		
	def process_physic(self):
		self.__calculate_delta_time()
		for obj in self.obj_on_screen:
			obj.update(self.delta_time_seconds)
		self.player.update(self.delta_time_seconds)
