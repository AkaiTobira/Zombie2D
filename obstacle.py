import pygame

from events import *

class Obstacle:

	state = "Const"

	r     = 0.0
	pos   = [0.0,0.0]
	color = (0,0,0)
	thick = 0.0
	current_screen = None
	
	def __init__(self, color, position, radius, thickness, screen):
		self.r     			= radius
		self.pos   			= position
		self.color			= color
		self.thick			= thickness
		self.current_screen = screen
		
		print ( self.r, self.pos, self.color ) 
	
	def set_screen(self, screen):
		self.current_screen = screen
	
	def set_position(self, position):
		self.pos = position
		
	def change_color(self, color):
		self.color = color

	def resize(self, radius):
		self.r = radius
		
	def draw(self):
		pygame.draw.circle(self.current_screen, self.color, self.pos, self.r, self.thick )
		
	def __move(self, speed):
		self.pos[0] += speed[0]
		self.pos[1] += speed[1]
		
	def process_event(self,event):
		pass
		
	def process_physic(self):
		pass
		
	def update(self, delta):
		pass