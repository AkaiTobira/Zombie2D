import pygame

from events import Events, rise_event
from random import randint
from colors import Colors, get_color
from vector import Vector
from ai     import *

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
	state 			 = "E"
	triggered         = False
	visible			  = True
	is_dead           = False

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
		self.ai.set_current_state(SteringWander())
		self.need_target       = True
		self.can_react         = True
		self.mouse_point      = Vector(0,0)
		self.closest_hideout  = None

		self.triggered         = False
		self.visible		   = True
		self.is_dead           = False


	def solve(self, P1, P2, P3, P4):
		nominatorA = (P4.x - P3.x)*(P1.y - P3.y) - (P4.y - P3.y)*(P1.x - P3.x)
		nominatorB = (P2.x - P1.x)*(P1.y - P3.y) - (P2.y - P1.y)*(P1.x - P3.x)
		denominator = (P4.y - P3.y)*(P2.x - P1.x) - (P4.x - P3.x)*(P2.y - P1.y)

		if denominator == 0 : return None

		uA = nominatorA / denominator
		uB = nominatorB / denominator

		if uA < 0 or uA > 1 : return None
		if uB < 0 or uB > 1 : return None

		return Vector( 
			P1.x + uA * (P2.x - P1.x),
			P1.y + uA * (P2.y - P1.y))


	def lin_function(self, pt_from, pt_to):
		lin_fun = Vector(0,0) 
		lin_fun.x = (pt_from.y - pt_to.y) / (pt_from.x - pt_to.x)
		lin_fun.y = pt_from.y - lin_fun.x * pt_from.x
		return lin_fun # zwraca parametry a i b funkcji		
	
	def intersection_points(self, P, r, f):
		a = 1 + f.x * f.x
		b = 2 * f.x * f.y - 2 * f.x * P.y - 2 * P.x
		c = - r * r + P.x * P.x + f.y * f.y - 2 * f.y * P.y + P.y * P.y

		x1 = (- b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
		x2 = (- b + math.sqrt(b * b - 4 * a * c)) / (2 * a)

		y1 = f.x * x1 + f.y
		y2 = f.x * x2 + f.y

		return [Vector(x1, y1), Vector(x2, y2)]	

	def process_event(self, event):
		if event.type == pygame.MOUSEMOTION:
			self.mouse_point = Vector(event.pos[0], event.pos[1])

		if event.type == Events.HIT_ENEMY_CHECK:
			shoot_line = self.lin_function(event.pt_from, event.pt_to)

			a = shoot_line.x * -1
			b = self.current_position.y - a * self.current_position.x
			enemy_line = Vector(a,b)
		#	enemy_line to prosta prostopadla do linii strzalu i przechodzaca przez srodek wroga

			enemy_points = self.intersection_points(self.current_position, self.RADIUS, enemy_line)

			point = self.solve(event.pt_from, event.pt_to, enemy_points[0], enemy_points[1])

			if point is not None:
				self.is_dead = True

		
	def update(self,delta):
		self.previous_position = self.current_position	
		self.current_position += self.velocity * delta

	def draw(self):
		if self.visible and not self.is_dead and not self.triggered :
			pygame.draw.circle(self.current_screen, self.COLOR, self.current_position.to_table(), self.RADIUS, self.THICKNESS )
		elif not self.visible:
			pass
	#		pygame.draw.circle(self.current_screen, get_color(Colors.DARK_YELLOW), self.current_position.to_table(), self.RADIUS, self.THICKNESS )
		elif self.triggered:
			pygame.draw.circle(self.current_screen, get_color(Colors.YELLOW), self.current_position.to_table(), self.RADIUS, self.THICKNESS )
		else :
			pygame.draw.circle(self.current_screen, get_color(Colors.RED), self.current_position.to_table(), self.RADIUS, self.THICKNESS )

	#	pygame.draw.line(self.current_screen, get_color(Colors.RED),self.current_position.to_table(), ( self.current_position + self.velocity).to_table(), 2 )
	#	pygame.draw.line(self.current_screen, get_color(Colors.BLUE),Vector(512,0).to_table(), Vector(512,720).to_table(), 2 )