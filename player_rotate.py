import pygame

from events import Events, rise_event

from vector import Vector
from random import randint
from colors import Colors, get_color

import math


class Player_rotate:

	rotation_angle  = 0.0
	rotation_change = False