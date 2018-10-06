import pygame

from events import *
from random import *

class Enemy:

	distance = Vector(0.0,0.0)
	move     = Vector(1.0,1.0)
	speed = 1
	
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
	
		pass
		
	def update(self, delta):
	
		if self.distance.is_zero_len() :
			self.distance = Vector( randint(0,100), randint(0,100) )
			self.move.x = randint(-1,1)
			self.move.y = randint(-1,1)
			
		if self.move.x == 0 :
			self.distance.x = 0
			
		
		if self.move.y == 0 :
			self.distance.y = 0
			
		if self.distance.x > 0 :
			self.pos[0] =  self.pos[0] + self.move.x
			self.distance.x -= self.move.x
		else :
			self.distance.x = 0

			
		if self.distance.y > 0 :
			self.pos[1] =  self.pos[1] + self.move.y
			self.distance.y -= self.move.y
		else :
			self.distance.y = 0

	
		pass