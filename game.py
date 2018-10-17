import pygame


from obstacle  import Obstacle as Ob 
from vector    import Vector 
from physic    import UnitManager
from generator import ObjectsGenerator, Sandbox
from colors    import Colors, get_color
from hud       import HUD

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
		self.HUD 		   = HUD(self.screen, self.player)		
	
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
			self.HUD.process_event(event)
			
		
	def __calculate_delta_time(self):
		delta = pygame.time.get_ticks() - self.delta_time_ticks
		self.delta_time_ticks = delta
		self.delta_time_seconds = delta/100000.0

	#	print( self.delta_time_seconds )
		
		
	def process_physic(self,delta):
		self.__calculate_delta_time()
		self.unitManager.process_physic(delta)
	#	print(delta)

