import pygame

from events import *

class Player:

	r     = 0.0
	pos   = [0.0,0.0]
	color = (0,0,0)
	current_screen = None
	
	def __init__(self,color,position,radius, screen):
		self.r     			= radius
		self.pos   			= position
		self.color			= color
		self.current_screen = screen
	
	def draw(self):
		pygame.draw.circle(self.current_screen,  self.color, self.pos, self.r )
		
	def process_event(self,event):
	
		if event.type == Events.CREATE:
			print( event.name )
	
		pass
		
	def process_physic(self):
		pass
		
	def update(self, delta):
		pass