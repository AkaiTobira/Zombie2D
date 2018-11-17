import pygame

from events import Events, rise_event
from random import randint
from colors import Colors, get_color
from vector import Vector
from ai     import *

class Enemy:
	THICKNESS = 6
	RADIUS    = 6
	COLOR     = get_color(Colors.LIGHT_BLUE)
	
	
	start_distance    = Vector(0.0,0.0)
	accumulate        = Vector(0.0,0.0)
	start_position    = Vector(0.0,0.0) 
	velocity          = Vector(0.0,0.0)
	
	current_screen = None
	current_position  = Vector(0.0,0.0)
	previous_position = Vector(0.0,0.0)
	
	seing_ahead       = Vector(0.0,0.0)
	seing_ahead_short = Vector(0.0,0.0)
	f                 = Vector(0.0,0.0)
	id          = -1

	destination = Vector(0.0,0.0)
	distance    = Vector(0.0,0.0)
	move        = Vector(1.0,1.0)
	speed       = Vector(35,35)
	
	screen_size = Vector(0,0)
	
	state       = "Wait"
	
	def __move(self, velocity, delta):
		self.previous_position     = self.current_position
		self.current_position      += ( velocity*delta )*self.speed
	
	
	def __init__(self, screen, screen_size, id):

		self.current_screen   = screen
		self.screen_size      = screen_size
		self.current_position = Vector(randint(0,self.screen_size.x), randint(0,self.screen_size.y))
		self.previous_position= self.current_position
		
		self.destination      = self.current_position
		self.id               = id
		
		self.distance         = Vector(0.0,0.0)
		self.accumulate       = Vector(0.0,0.0)
	
	
	def draw(self):
	
		#pygame.draw.line(self.current_screen, get_color(Colors.BLACK),self.start_position.to_table(), self.destination.to_table() )
	
		pygame.draw.circle(self.current_screen, self.COLOR, self.current_position.to_table(), self.RADIUS, self.THICKNESS )
		
		# draw destination
		#pygame.draw.line(self.current_screen, get_color(Colors.RED),self.current_position.to_table(), self.destination.to_table() )
		
		# draw velocity
		#pygame.draw.line(self.current_screen, get_color(Colors.GREEN),self.current_position.to_table(),(self.current_position + self.f + self.distance.norm() ).to_table())

		#pygame.draw.line(self.current_screen, get_color(Colors.BLUE),self.current_position.to_table(),(self.current_position + self.velocity ).to_table())

		
		# draw shorter ahead
		#pygame.draw.line(self.current_screen, get_color(Colors.GREEN),self.current_position.to_table(),(self.seing_ahead).to_table())
		# draw longer  ahead
		#pygame.draw.line(self.current_screen, get_color(Colors.BLUE),self.current_position.to_table(),(self.seing_ahead_short).to_table())
		
		
	def process_event(self,event):
	
		if event.type == Events.COLLIDE:
			self.stop_unit()
			self.current_position = event.where
			
			if event.stuck :
				self.current_position = Vector(randint(0,self.screen_size.x), randint(0,self.screen_size.y))
				self.previous_position   = self.current_position
			return 
		
	def apply_force(self, f):
		self.f = f
		pass
		
	def stop_unit(self):
		self.current_position = self.previous_position 
		self.destination      = self.current_position
		self.velocity         = Vector(0.0,0.0)
		self.state            = "Wait"
	
	def move_to(self, destination):
		self.start_position = self.current_position
		self.start_distance = self.current_position.distance_to(self.destination)
		self.state       = "Move"
		self.destination = destination
		self.velocity = self.current_position.distance_to(self.destination).norm() * self.speed
		
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
				self.accumulate = Vector(0.0,0.0)
		
	def __accumulate(self):
	
		if self.current_position.distance_to(self.destination).len() <=  self.start_distance.len()/2:
			self.accumulate +=  Vector(1,1)
		else:
			self.accumulate -=  Vector(1,1)
		
	def update(self, delta):
			if self.state == "Move":
				desired_velocity = self.current_position.distance_to(self.destination).norm()# * self.speed
	#			
	#			self.seing_ahead       = self.current_position + self.velocity * self.speed * 10
	#			self.seing_ahead_short = self.current_position + self.velocity * self.speed * (10/2)
				
				steeing = desired_velocity - self.velocity  # + self.f.norm() * self.speed
				
	#			steeing.trunc(Vector(1,1))
				
				velocity = ((self.velocity + steeing) + self.accumulate * 10)
			
				self.velocity_vector = velocity * 10 
			
	#			self.seing_ahead = self.seing_ahead * (velocity.len() / self.speed)
	#			self.seing_ahead_short = self.seing_ahead_short * (velocity.len() / self.speed)
			
	#		
	#			velocity = (self.velocity + self.f) * self.speed 
	#			self.distance = self.current_position.distance_to(self.destination)
	#			left_distance = self.distance.abs() - velocity.abs()
	#			self.distance -= velocity
#
				distance = self.current_position.distance_to(self.destination).abs() - velocity.abs()

				self.__check_stop(distance)
				self.__move(velocity, delta)
				pass

class Enemy2:
	THICKNESS = 6
	RADIUS    = 6
	COLOR     = get_color(Colors.LIGHT_BLUE)

	current_screen    = None
	current_position  = Vector(0,0)
	velocity          = Vector(0,0)
	ai                = None
	max_speed         = Vector(50,50)
	m                 = 1
	closest_obstacle  = None

	ahead             = Vector(0,0)

	priorities        = [0.05, 0.7, 0.5]

	triggered         = False

	def __init__(self,  screen, screen_size, id):

		self.current_screen   = screen
		self.screen_size      = screen_size
		self.current_position = Vector(randint(0,self.screen_size.x), randint(0,self.screen_size.y))
		self.previous_position= self.current_position
		
		self.destination      = self.current_position
		self.id               = id
		
		self.distance         = Vector(0.0,0.0)
		self.accumulate       = Vector(0.0,0.0)

		self.ai 			  = FiniteStateMachine(self)
		self.ai.set_current_state(TestBehaviour())
		self.need_target       = True
		self.mouse_point      = Vector(0,0)
		self.teammate         = self

	def process_event(self, event):
		if event.type == pygame.MOUSEMOTION:
			self.mouse_point = Vector(event.pos[0], event.pos[1])
		pass

	def update(self,delta):
		self.previous_position = self.current_position	
		self.current_position += self.velocity * delta

	def draw(self):
		pygame.draw.circle(self.current_screen, self.COLOR, self.current_position.to_table(), self.RADIUS, self.THICKNESS )

		pygame.draw.line(self.current_screen, get_color(Colors.RED),self.current_position.to_table(), ( self.current_position + self.velocity).to_table(), 2 )
		pygame.draw.line(self.current_screen, get_color(Colors.BLUE),Vector(512,0).to_table(), Vector(512,720).to_table(), 2 )