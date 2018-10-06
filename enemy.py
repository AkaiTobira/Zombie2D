import pygame

from events import *
from random import *
from colors import *

class Enemy:
	id          = 1

	destination = Vector(0.0,0.0)
	distance    = Vector(0.0,0.0)
	move        = Vector(1.0,1.0)
	speed       = 3
	
	r           = 0.0
	position    = Vector(0.0,0.0)
	color       = (0,0,0)
	thick       = 0.0
	current_screen = None
	screen_size = Vector(0,0)
	
	state       = "Wait"
	
	def __move(self, velocity ,delta):
		self.position      += velocity
	
	
	def __init__(self, color , radius, thickness, screen, screen_size):
		self.r     			= radius
		self.color			= color
		self.thick			= thickness
		self.current_screen = screen
		self.position       = Vector(randint(0,screen_size.x), randint(0,screen_size.y))
		self.screen_size    = screen_size
		self.destination    = self.position
		self.distance       = Vector(0.0,0.0)
	
	def draw(self):
		pygame.draw.circle(self.current_screen, self.color, self.position.to_table(), self.r, self.thick )
		pygame.draw.line(self.current_screen, get_color(Colors.RED),self.position.to_table(), self.destination.to_table() )
		pygame.draw.line(self.current_screen, get_color(Colors.GREEN),self.position.to_table(),(self.position + self.distance.norm() * 20 * self.speed).to_table())
		
		
	def process_event(self,event):
	
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 3:
				self.state = "Move"
				self.destination = Vector( randint(0,self.screen_size.x), randint(0,self.screen_size.y) )
				self.distance = self.position.distance_to(self.destination)
	
		pass
		
	def __check_stop(self, left_distance):
		stop = False
		if left_distance.x <= 0:
			self.distance.x = 0
			stop = True
				
		if left_distance.x <= 0:
			self.distance.y = 0

			if stop :
				self.state = "Wait"
				self.position = self.destination
		
	def update(self, delta):
			if self.state == "Move":
				velocity = self.distance.norm() * self.speed
				left_distance = self.distance.abs() - velocity.abs()
				self.distance -= velocity

				self.__check_stop(left_distance)
				self.__move(velocity, delta)
