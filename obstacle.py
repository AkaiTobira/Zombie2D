import pygame

import math
from events   import Events, rise_event
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

#		points = self.intersection_points(Vector(3,2), 2, Vector(0,2))
#		print(str(points[0]))
#		print(str(points[1]))


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
		if(position.x >= 462 and position.x <= 562 and position.y >= 310 and position.y <= 410): 
		# player start position: Vector(512,360)
			position = self.random_position() 
		return position	


	def check_position(self, other):
		distance = (self.current_position - other.current_position).len()
		if distance > (self.RADIUS + other.RADIUS): return True
		else: return False


	def draw(self):
		pygame.draw.circle(self.current_screen, get_color(Colors.LIGHT_PURPL2), self.current_position.to_table(), self.RADIUS)
		pygame.draw.circle(self.current_screen, self.COLOR_OUT, self.current_position.to_table(), self.RADIUS, self.THICK )
		
	def calc_distance(self, point, f):
		return ( abs(f.x * point.x - point.y + f.y) ) / ( math.sqrt(f.x * f.x + 1) )

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

	def process_event(self,event):

		if event.type == Events.SHOOT:

			shoot_line = self.lin_function(event.pt_from, event.pt_to)

			a = shoot_line.x * -1
			b = self.current_position.y - a * self.current_position.x
			obst_line = Vector(a,b)
		#	obst_line to prosta prostopadla do linii strzalu i przechodzaca przez srodek przeszkody

			obs_points = self.intersection_points(self.current_position, self.RADIUS, obst_line)

			point = self.solve(event.pt_from, event.pt_to, obs_points[0], obs_points[1])

			if point is None:
				point = event.pt_to

			rise_event( Events.INTERSECTION, { "point" : point } )
		
		
	def process_physics(self):
		pass
		
	def update(self, delta):
		pass