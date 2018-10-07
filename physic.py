import pygame

class UnitManager:
	entity_list = []
	
	player      = None
	screen      = None 
	mv_system   =  None
	cl_system   =  None
	
	def __init__(self, units, player, screen):
		self.entity_list      = units
		self.screen           = screen
		self.mv_system        = MoveSystem(units)
		self.cl_system        = CollisionSystem(units)
		self.player           = player
		
	def draw(self):
		self.screen.fill((20,30,47))
		for obj in self.entity_list:
			obj.draw()
		self.player.draw()
		pygame.display.flip()
		
	def process_input(self,event):
		for obj in self.entity_list:
			obj.process_event(event)
			self.player.process_event(event)
		pass
		
	def process_physic(self,delta):
		for obj in self.entity_list:
			obj.update(delta)
			self.player.update(delta)
		pass
	
	def add_unit(self,unit):
		entity_list.append(unit)
		
	
	
class MoveSystem:
	def __init__(self, units):
		pass

	
class CollisionSystem:
	def __init__(self, units):
		pass
	pass
	
