import pygame

from events   import Events
from random   import randint
from vector   import Vector
from colors   import Colors, get_color

class Obstacle:
	RADIUS 			 = 0
	COLOR_OUT 		 = get_color(Colors.LIGHT_PURPLE)
	THICK  			 = 2

	id 			 	 = -1
	state 			 = "Const"

	color 			 = (0,0,0)
	thick 			 = 0.0
	current_screen   = None
	screen_size		 = Vector(0,0) 
	current_position = Vector(0,0)
	velocity         = Vector(0,0)
	
	
	def __init__(self, screen, screen_size, id, obs_list):
		self.RADIUS = randint(15,35) 
		self.current_screen   = screen
		self.screen_size = screen_size
		
		self.id               = id
		self.set_position(obs_list)


	def set_position(self, obs_list):

		if len(obs_list) == 0:
			self.current_position = self.random_position()

		else:	
			self.current_position = self.random_position()
			for i in range(len(obs_list)):
				if not self.check_position(obs_list[i]):
					self.current_position = self.random_position()
					self.set_position(obs_list)


	def random_position(self):
		position = Vector( randint(0, self.screen_size.x), randint(0, self.screen_size.y))
		if(position.x >= 462 and position.x <= 562 and position.y >= 310 and position.y <= 410): # player start position: Vector(512,360)
			position = self.random_position() 
		return position	


	def check_position(self, other):
		distance = (self.current_position - other.current_position).len()
		if distance > (self.RADIUS + other.RADIUS): return True
		else: return False


	def draw(self):
	#	pygame.draw.circle(self.current_screen, get_color(Colors.LIGHT_PURPL2), self.current_position.to_table(), self.RADIUS)

		pygame.draw.circle(self.current_screen, self.COLOR_OUT, self.current_position.to_table(), self.RADIUS, self.THICK )
		
	def process_event(self,event):
		pass
		
	def process_physics(self):
		pass
		
	def update(self, delta):
		pass