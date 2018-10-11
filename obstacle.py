import pygame

from events   import Events
from random   import randint
from vector   import Vector
from colors   import Colors, get_color

class Obstacle:
	RADIUS = 0
	COLOR  = get_color(Colors.LIGHT_PURPLE)
	THICK  = 2

	id = -1
	state = "Const"

	pos   = [0.0,0.0]
	color = (0,0,0)
	thick = 0.0
	current_screen = None
	current_position = Vector(0,0)
	velocity         = Vector(0.,0.)
	
	
	def __init__(self, screen, screen_size, id):
		self.COLOR  = get_color(Colors.LIGHT_PURPLE)
		self.RADIUS = randint(15,30) 
		self.current_screen   = screen
		self.pos   			  = [randint(0,screen_size.x), randint(0,screen_size.y)]
		
		self.id               = id
		self.current_position = Vector(self.pos[0],self.pos[1])
		
	def draw(self):
		pygame.draw.circle(self.current_screen, self.COLOR, self.pos, self.RADIUS, self.THICK )
		
	def process_event(self,event):
		pass
		
	def process_physic(self):
		pass
		
	def update(self, delta):
		pass