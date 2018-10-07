import pygame

from events import *
from random import *
from colors import *

class Enemy:
	THICKNESS = 6
	RADIUS    = 6
	COLOR     = get_color(Colors.LIGHT_BLUE)
	
	current_screen = None
	current_position  = Vector(0.0,0.0)
	previous_position = Vector(0.0,0.0)
	

	id          = 1

	destination = Vector(0.0,0.0)
	distance    = Vector(0.0,0.0)
	move        = Vector(1.0,1.0)
	speed       = 3
	
	screen_size = Vector(0,0)
	
	state       = "Wait"
	
	def __move(self, velocity ,delta):
		self.current_position      += velocity
	
	
	def __init__(self,  screen, screen_size):

		self.current_screen   = screen
		self.current_position = Vector(randint(0,screen_size.x), randint(0,screen_size.y))
		self.previous_position= self.current_position
		
		self.screen_size      = screen_size
		self.destination      = self.current_position
		self.distance         = Vector(0.0,0.0)
	
	def draw(self):
		pygame.draw.circle(self.current_screen, self.COLOR, self.current_position.to_table(), self.RADIUS, self.THICKNESS )
		pygame.draw.line(self.current_screen, get_color(Colors.RED),self.current_position.to_table(), self.destination.to_table() )
		pygame.draw.line(self.current_screen, get_color(Colors.GREEN),self.current_position.to_table(),(self.current_position + self.distance.norm() * 20 * self.speed).to_table())
		
		
	def process_event(self,event):
	
	
		pass
		
	def move_by(self, velocity, destination):
		self.state       = "Move"
		self.destination = destination
		self.distance    = self.current_position.distance_to(self.destination)
		self.velocity    = velocity
		
	def __check_stop(self, left_distance):
		stop = False
		if left_distance.x <= 0:
			self.distance.x = 0
			stop = True
				
		if left_distance.x <= 0:
			self.distance.y = 0

			if stop :
				self.state = "Wait"
				self.current_position = self.destination
		
	def update(self, delta):
			if self.state == "Move":
				velocity = self.velocity * self.speed
				left_distance = self.distance.abs() - velocity.abs()
				self.distance -= velocity

				self.__check_stop(left_distance)
				self.__move(velocity, delta)
