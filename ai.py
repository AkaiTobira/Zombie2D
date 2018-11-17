from random import randint, uniform
from vector import Vector
import math

class FiniteStateMachine:
    current_state  = None
    previous_state = None
    global_state   = None 
    owner          = None 

    def __init__(self, owner):
        self.owner = owner

    def set_current_state(self, state):
        self.current_state = state
    def set_global_state(self, state):
        self.global_state = state
    def set_previous_state(self, state):
        self.previous_state = state

    def change_state(self, state):
        self.previous_state = self.current_state
        self.current_state.exit(self.owner)
        self.current_state  = state
        self.current_state.enter(self.owner)

    def update(self,delta,position):
        if self.current_state:
            self.current_state.execute(self.owner,position)

    def revert_to_previous_state(self):
        self.change_state(self.previous_state)

    def is_in_state(self,state):
        return state == self.current_state
        
class State:
    state = "None"
    w_target          = Vector(0,0) 

    walls           = [ 
            [ Vector(0    ,   0), Vector(1024,0), Vector( 0 , 1)],
            [ Vector(0    ,   0), Vector(0, 720), Vector( 1 , 0)],
            [ Vector(1024,0),    Vector(1024 , 720),  Vector( -1 , 0 )],
            [  Vector(0, 720),   Vector(1024 , 720), Vector( 0, -1)]
            ]

    def __eq__(self,state):
        return state == self.state

    def wander(self,owner, player):
        w_r        = 3
        w_distance = 3
        w_jiter    = 4

        self.w_target += Vector(uniform(-1, 1) * w_jiter, uniform(-1, 1) * w_jiter ).norm() * w_r
        target_local  = self.w_target + Vector(w_distance, 0) 
        return self.seek(owner, owner.current_position.to_global_space(target_local))

    def seek(self, owner, target):
        velocity =  (target- owner.current_position).norm() * owner.max_speed     - owner.velocity
        return velocity

    def arrival(self, owner, target):
        distance = owner.current_position.distance_to(target.current_position)
        velocity =  (target.current_position- owner.current_position).norm() * owner.max_speed     - owner.velocity
        return min( velocity , distance ) 

    def avoid(self, owner, target):
        if owner.closest_obstacle and not owner.velocity.is_zero_len() :
            av_f = owner.ahead - owner.closest_obstacle.current_position                        
            return av_f.norm() * 40
        return Vector(0,0)

    def solve( self, P1, P2, P3, P4):
        nominatorA  =  (P4.x - P3.x)*(P1.y - P3.y) - (P4.y - P3.y)*(P1.x - P3.x)
        nominatorB  =  (P2.x - P1.x)*(P1.y - P3.y) - (P2.y - P1.y)*(P1.x - P3.x)
        denominator =  (P4.y - P3.y)*(P2.x - P1.x) - (P4.x - P3.x)*(P2.y - P1.y)

        if denominator == 0 : return None

        uA = nominatorA/denominator
        uB = nominatorB/denominator

        if uA < 0 or uA > 1 : return None
        if uB < 0 or uB > 1 : return None
        
        return Vector( P1.x + uA*(P2.x-P1.x), P1.y + uA*(P2.y-P1.y) )


    def wallcheckTest(self,owner,player):
        fleevers           = [ owner.velocity * 5 , owner.velocity.rotate(math.pi/8)*5, owner.velocity.rotate(-math.pi/8)*5 ]
        stering            = Vector(0,0)
        c_wall             = None
        c_distance_to_wall = 999999999
        c_point            = None

        for f in fleevers:
            point = self.solve( owner.current_position, owner.current_position + f, Vector(512, 0),Vector(512,720))
            if point is None : continue
   
            distance_to_wall = point.distance_to(owner.current_position).len()
            if distance_to_wall < c_distance_to_wall: 
                c_distance_to_wall = distance_to_wall
                c_point            = point 
                c_wall             = [[],[],Vector(-1,0 )]

            if c_wall :
                over_shot = f - c_point 
                stering   += c_wall[2] * over_shot.len() * 3
                print( stering )

        return stering

    def wallcheck(self,owner,player):
        fleevers           = [ owner.velocity * 3 ]# , owner.velocity.rotate(math.pi/8)*3, owner.velocity.rotate(-math.pi/8)*3 ]
        stering            = Vector(0,0)
        c_wall             = None
        c_distance_to_wall = 999999999
        c_point            = None

        for f in fleevers:
            for wall in self.walls:
                point = self.solve( owner.current_position, owner.current_position + f, wall[0],wall[1])
                if point is None : continue
   
                distance_to_wall = point.distance_to(owner.current_position).len()
                if distance_to_wall < c_distance_to_wall:
                    c_distance_to_wall = distance_to_wall
                    c_point            = point 
                    c_wall             = wall

            if c_wall :
                over_shot = f - c_point 
                stering   += c_wall[2] * over_shot.len() #* 10
    #            print( stering )

        return stering


class EvadeWander(State):
    state = "Wander"

    max_stering_force = Vector(22,22)

    def calculate_steering(self, owner, player):
        stering = -self.arrival(owner,player)     *  owner.priorities[0]
        stering += self.avoid(owner,player)       *  owner.priorities[1]
        stering += self.wallcheck(owner,player)   *  owner.priorities[2]
        stering  = stering.ttrunc(self.max_stering_force)

        return stering


    def enter(self, owner):
        pass


    def exit(self, owner):
        pass

    def execute(self, owner, player):
        stering_force  = self.calculate_steering(owner, player)
        owner.velocity =  ( owner.velocity + stering_force / owner.m ).ttrunc( owner.max_speed)


        if owner.current_position.distance_to(player.current_position).len() > 200 :
            owner.ai.change_state( SteringWander() )

        pass

class SteringWander(State):
    state = "Wander"

    max_stering_force = Vector(22,22)

    def calculate_steering(self, owner, player):
        stering   = self.wander(owner,player)  *  owner.priorities[0]
        stering  += self.avoid(owner,player)       *  owner.priorities[1]
        stering   += self.wallcheck(owner,player)  *  owner.priorities[2]
        stering   = stering.ttrunc(self.max_stering_force)

        return stering


    def enter(self, owner):
        pass


    def exit(self, owner):
        pass

    def execute(self, owner, player):
        stering_force  = self.calculate_steering(owner, player)
        owner.velocity =  ( owner.velocity + stering_force / owner.m ).ttrunc( owner.max_speed)
        pass

class StateSteeringBehaviour(State):
    state = "Stering"

    max_stering_force = Vector(22,22)
    w_target          = Vector(0,0)

    def wander(self,owner, player):
        w_r        = 3
        w_distance = 3
        w_jiter    = 2

        self.w_target += Vector(uniform(-1, 1) * w_jiter, uniform(-1, 1) * w_jiter ).norm() * w_r
        target_local  = self.w_target + Vector(w_distance, 0) 
        return self.seek(owner, owner.current_position.to_global_space(target_local))

    def seek(self, owner, target):
        distance = target.distance_to(owner.current_position)
        velocity =  (target- owner.current_position).norm() * owner.max_speed     - owner.velocity
        return min( velocity , distance ) 




    def calculate_steering(self, owner, player):
        stering  = self.wander(owner,player)       *  owner.priorities[0]
     #   stering += self.avoid(player)        *  owner.priorities[1]
    #   stering += self.separation(player)   *  owner.priorities[2]
        return stering

    def enter(self, owner):
        pass

    def exit(self, owner):
        pass

    def execute(self, owner, player):
        stering_force = self.calculate_steering(owner, player)
        owner.velocity = stering_force / owner.m

        if abs(owner.velocity.x) > owner.max_speed.x: owner.velocity.x = sign(owner.velocity.x) * owner.max_speed.x
        if abs(owner.velocity.y) > owner.max_speed.y: owner.velocity.y = sign(owner.velocity.y) * owner.max_speed.y

        pass

class TestBehaviour(State):

    max_stering_force = Vector(22,22)
    w_target          = Vector(0,0) 


    def wallcheckTest(self,owner,player):
        fleevers           = [ owner.velocity * 5 , owner.velocity.rotate(math.pi/8)*5, owner.velocity.rotate(-math.pi/8)*5 ]
        stering            = Vector(0,0)
        c_wall             = None
        c_distance_to_wall = 999999999
        c_point            = None

        for f in fleevers:
            point = self.solve( owner.current_position, owner.current_position + f, Vector(512, 0),Vector(512,720))
            if point is None : continue
   
            distance_to_wall = point.distance_to(owner.current_position).len()
            if distance_to_wall < c_distance_to_wall: 
                c_distance_to_wall = distance_to_wall
                c_point            = point 
                c_wall             = [[],[],Vector(-1,0 )]

            if c_wall :
                over_shot = f - c_point 
                stering   += c_wall[2] * over_shot.len() * 3
                print( stering )

        return stering

    
    def calculate_steering(self, owner, player):
        stering = self.arrival(owner, owner.teammate) *  owner.priorities[0]
    #    stering = self.wander(owner,player)  *  owner.priorities[0]
    #    stering   = self.arrival(owner,player) #      *  owner.priorities[0]

        stering  += self.avoid(owner,player)       *  owner.priorities[1]

    #    print("Current Stering :", stering)

        stering   += self.wallcheck(owner,player)  *  owner.priorities[2]
     #   stering   += self.wallcheckTest(owner,player)

    #    print("Updated by wallcheck :", stering)

        stering   = stering.ttrunc(self.max_stering_force)

        return stering

    def enter(self, owner):
        pass


    def exit(self, owner):
        pass

    def execute(self, owner, player):
        stering_force  = self.calculate_steering(owner, player)
        owner.velocity =  ( owner.velocity + stering_force / owner.m ).ttrunc( owner.max_speed)

        if owner.teammate.current_position.distance_to( owner.current_position).len() < 5:
            owner.need_target = True
        pass

class PlayerHunt(State):

    max_stering_force = Vector(22,22)
    w_target          = Vector(0,0) 
    walls           = [ 
            [ Vector(0    ,   0), Vector(1024,0), Vector( 0 , 1)],
            [ Vector(0    ,   0), Vector(0, 720), Vector( 1 , 0)],
            [ Vector(1024,0),    Vector(1024 , 720),  Vector( -1 , 0 )],
            [  Vector(0, 720),   Vector(1024 , 720), Vector( 0, -1)]
            ]

    def calculate_steering(self, owner, player):
        stering = self.arrival(owner,player)  *  owner.priorities[0]
    #    stering   = self.arrival(owner,player) #      *  owner.priorities[0]

        stering  += self.avoid(owner,player)       *  owner.priorities[1]

    #    print("Current Stering :", stering)

        stering   += self.wallcheck(owner,player)  *  owner.priorities[2]
     #   stering   += self.wallcheckTest(owner,player)

    #    print("Updated by wallcheck :", stering)

        stering   = stering.ttrunc(self.max_stering_force)

        return stering

    def enter(self, owner):
        pass


    def exit(self, owner):
        pass

    def execute(self, owner, player):
        stering_force  = self.calculate_steering(owner, player)
        owner.velocity =  ( owner.velocity + stering_force / owner.m ).ttrunc( owner.max_speed)
        pass

