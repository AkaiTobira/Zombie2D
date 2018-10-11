import pygame

from events import Events, rise_event

from player import Player
from vector import Vector
from random import randint
from colors import Colors, get_color

import math


class Player_move:

	current_position  = Vector(0,0)
	previous_position = Vector(0,0)
	velocity          = Vector(0,0)

	direction 		= "up"

	key_pressed     = { 
						"up"   : 
						{ 
							"scancode": [72, 17],
							"enable"  : False,
							"velocity": Vector(0.0, -1.0)
						},
						"down"   : 
						{ 
							"scancode": [80, 31],
							"enable"  : False,
							"velocity": Vector(0.0, 1.0)
						},
						"left"   : 
						{ 
							"scancode": [77, 32],
							"enable"  : False,
							"velocity": Vector(1.0, 0.0)
						},
						"right"   : 
						{ 
							"scancode": [75, 30],
							"enable"  : False,
							"velocity": Vector(-1.0, 0.0)
						}
					}	

