
from enum import Enum

class Colors(Enum):
	LIGHT_BLUE   = (24,191,158)
	LIGHT_PURPLE = (159,133,188)
	LIGHT_RED    = (255,21,82)
	
def get_color( color ):
	if color == Colors.LIGHT_BLUE:
		return (24,191,158)
	if color == Colors.LIGHT_PURPLE:
		return (159,133,188)
	if color == Colors.LIGHT_RED:
		return (255,21,82)