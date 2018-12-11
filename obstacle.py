import pygame

import math
from events   import Events, rise_event
from random   import randint
from vector   import Vector
from colors   import Colors, get_color

class Triangle:
	vertices = []
	basic    = [] 
	position = Vector(0,0)
	def __init__(self, size):
		self.vertices = [Vector(0.0,-1.0)*size, Vector(-0.7,1.0)*size, Vector(0.7,1.0)*size]
		self.basic = self.vertices.copy()
		
	def rotate(self, angle):
		for i in range(len(self.vertices)):
			self.vertices[i] = self.basic[i].rotate(angle)
		
	def scale_back_line(self, number):
		temp        = self.basic[0] 

		self.basic[0] = self.basic[0] * number
		self.basic[1] = self.basic[1] * number
		self.basic[2] = self.basic[2] * number

		correction       = self.basic[0] - temp 

		for i in range(len(self.vertices)):
			self.basic[i] = self.basic[i]-correction


	def __sign(self, p1, p2, p3):
		return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

	def is_in_triangle(self, point):

		d1 = self.__sign(point, self.position + self.vertices[0], self.position + self.vertices[1] )
		d2 = self.__sign(point, self.position + self.vertices[1], self.position + self.vertices[2] )
		d3 = self.__sign(point, self.position + self.vertices[2], self.position + self.vertices[0] )
		
		has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
		has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

		return not (has_neg and has_pos)

	def to_draw(self, position):
		self.position = position
		return [ (position + self.vertices[0]).to_touple(),
				 (position + self.vertices[1]).to_touple(),
				 (position + self.vertices[2]).to_touple()]


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
	triangle         = None
	
	
	def __init__(self, screen, screen_size, id, obs_list):
		self.RADIUS = randint(15,35) 
		self.current_screen   = screen
		self.screen_size = screen_size
		
		self.id               = id
		self.set_position(obs_list)
		self.triangle         = Triangle(self.RADIUS)
		self.triangle.scale_back_line(1024)
		
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

		self.face 	  = Vector(self.current_position.x, self.current_position.y - 200)


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

	def draw_id_number(self):
		font = pygame.font.SysFont("consolas", self.RADIUS-3)

		text = font.render(str(self.id), True, self.COLOR_OUT)
		text_rect = text.get_rect(center=(self.current_position.x, self.current_position.y))
		self.current_screen.blit(text, text_rect)

	def draw(self):
		pygame.draw.circle(self.current_screen, get_color(Colors.LIGHT_PURPL2), self.current_position.to_table(), self.RADIUS)
		pygame.draw.circle(self.current_screen, self.COLOR_OUT, self.current_position.to_table(), self.RADIUS, self.THICK )
		pygame.draw.polygon (
			self.current_screen,  
			get_color(Colors.LIGHTER_RED), 
			self.triangle.to_draw(self.current_position),
			1)
	#	self.draw_id_number()	


	def is_in_shade(self, point):
		return self.triangle.is_in_triangle(point)

	def check_intersection(self, shoot_from, shoot_to):
		shot_dir = (shoot_to - shoot_from).norm()
		to_obs = self.current_position - shoot_from
		dot = shot_dir.dot(to_obs.norm())

		if dot <= 0 : return None
		else : 
			distance = (self.current_position - shoot_from - shot_dir * to_obs.len()).len()

			if distance > self.RADIUS : return None
			else : return shoot_from + shot_dir * to_obs.len()


	def process_event(self,event):

		if event.type == Events.SHOOT:

			point = self.check_intersection(event.pt_from, event.pt_to)

			if point is None:
				point = event.pt_to

			rise_event( Events.INTERSECTION, { "point" : point } )
		
	def set_player_position(self, position):
		self.player_position = position
		self.angle = (self.face - self.current_position).norm().angle_between((position - self.current_position).norm()) 

	def process_physics(self):
		pass
	
	angle = 0
	def update(self, delta):

		self.triangle.rotate(self.angle)
		
		pass