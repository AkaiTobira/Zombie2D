
import math 

class Vector:
	x = 0.0
	y = 0.0
	
	def __init__(self,x,y):
		self.x = x
		self.y = y
		
	def __rep__(self):
		return self.__str__
	
	def __add__(self, vec):
		return Vector(self.x + vec.x, self.y + vec.y)
		
	def __sub__(self, v):
		return Vector(self.x - v.x, self.y - v.y)
		
	def __neg__(self ):
		return Vector(-self.x, -self.y)

	def __str__(self):
		return "[" + str(self.x) + "," + str(self.y) + "]" 
		
	def __eq__(self, v):
		return self.x == v.x and self.y == v.y
		
	def __neq__(self,v):
		return not self == v
		
	def __mul__(self,v):
		if isinstance(v,(int,float)):
			return Vector(self.x*v, self.y*v)
		return Vector(self.x * v.x, self.y * v.y)
		
	def __rmul__(self,v):
		return self.__mul__(v)
			
	def dot(self,v):
		return self.x* v.x + self.y *v.y
		
	def len(self):
		return math.sqrt(self.x**2 + self.y**2)
		
	def distance_to(self,v):
		return Vector(v.x - self.x,  v.y - self.y)
		
	def abs(self):
		return Vector(math.fabs(self.x), math.fabs(self.y))
		
	def angle_between(self,v):
		return math.acos( self.dot(v) * ( 1.0 / ( v.len() + self.len() )  ))
		
	def is_zero_len(self):
		return self.x == 0.0 and self.y == 0.0
		
	def to_table(self):
		return [int(self.x), int(self.y)]
		
	def to_touple(self):
		return ( int(self.x), int(self.y) )
		
	def norm(self):
		if self.is_zero_len():
			return Vector(0.0,0.0)
		return self * (1/self.len())
	
	def trunc(self, v):
		return Vector( self.x if self.x < v.x else v.x, self.y if self.y < v.y else v.y ) 
		
	def rotate(self, angle, axis = None ):
		if axis == None:
			axis=Vector(0.0,0.0) 
		return Vector(
			(self.x - axis.x) * math.cos(angle) - (self.y - axis.y) * math.sin(angle) + axis.x,
			(self.x - axis.x) * math.sin(angle) + (self.y - axis.y) * math.cos(angle) + axis.y
			)
		
	def sign(self):
		return Vector( 1 if self.x > 0 else 0 if self.x == 0 else -1, 1 if self.y > 0 else 0 if self.y == 0 else -1  )