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

    def __eq__(self,state):
        return state == self.state

class SteringWander(State):
    state = "Wander"

    max_stering_force = Vector(22,22)
    w_target          = Vector(0,0) 
    walls           = [ 
            [ Vector(0    ,   0), Vector(1024,0), Vector( 0 , 1)],
            [ Vector(0    ,   0), Vector(0, 720), Vector( 1 , 0)],
            [ Vector(1024 , 720), Vector(1024,0), Vector( 0 , 1 )],
            [ Vector(1024 , 720), Vector(0, 720), Vector( 1, 0)]
            ]




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
        distance = owner.current_position.distance_to(target)
        velocity =  (target- owner.current_position).norm() * owner.max_speed     - owner.velocity
        return min( velocity , distance ) 

    def avoid(self, owner, target):
        if owner.closest_obstacle and not owner.velocity.is_zero_len() :
            av_f = owner.ahead - owner.closest_obstacle.current_position                        
            return av_f.norm() * 40
        return Vector(0,0)

    def lin_function(self, pt_from, pt_to):
        lin_fun = Vector(0,0) 
        lin_fun.x = (pt_from.y - pt_to.y) / (pt_from.x - pt_to.x)
        lin_fun.y = pt_from.y - lin_fun.x * pt_from.x
    #	print("function: " + str(lin_fun))
        return lin_fun # zwraca parametry a i b funkcji
	
    def solve_linerar( self, coon1, coon2):
       # b1.x + e1.x * t = b2.x + e2.x * u
       # b1.y + e1.y * t = b2.y + e2.y * u
        pass    
 

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
     #   print( P1, P2, P3, P4)
     #   print( uA, uB )
     #   print( Vector( P1.x + uA*(P2.x-P1.x), P1.y + uA*(P2.y-P1.y) ) )



    def wallcheck(self,owner,player):
        fleevers           = [ owner.velocity * 3 ]#, owner.velocity.rotate(math.pi/8)*3, owner.velocity.rotate(-math.pi/8)*3 ]
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
                    stering   += c_wall[2] * over_shot.len()

        return stering.ttrunc(self.max_stering_force)


    def calculate_steering(self, owner, player):
        stering   = self.wander(owner,player)       *  owner.priorities[0]

        print(stering)

        stering  += self.avoid(owner,player)        *  owner.priorities[1]

        print(stering)

        stering   += self.wallcheck(owner,player)

        print( stering)
        print( " _ ")
        stering   = stering.ttrunc(self.max_stering_force)
        stering   = stering - owner.velocity
    #   stering += self.separation(player)   *  owner.priorities[2]
        return stering

    def enter(self, owner):
        pass


    def exit(self, owner):
        pass

    def execute(self, owner, player):
        stering_force = self.calculate_steering(owner, player)
        owner.velocity += stering_force / owner.m

    #    if owner.current_position.distance_to(player.current_position).len() < 200:
    #        owner.ai.change_state(SeekState())

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
    walls           = [ 
            [ Vector(0    ,   0), Vector(1024,0), Vector( 0 , 1)],
            [ Vector(0    ,   0), Vector(0, 720), Vector( 1 , 0)],
            [ Vector(1024,0),    Vector(1024 , 720),  Vector( -1 , 0 )],
            [  Vector(0, 720),   Vector(1024 , 720), Vector( 0, -1)]
            ]




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
   
      #          print( "Collision find :", point)

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


class SeekState(State):
    state = "Seek"

    def enter(self, owner):
        pass

    def exit(self, owner):
        pass

    def avoid(self, owner, target):
        #TODO
        if owner.closest_obstacle :
            stering_force = Vector(0,0)

            t = owner.current_position + owner.velocity
            avoid_force = t - owner.closest_obstacle.current_position
            return avoid_force.norm() * owner.max_speed * 22

          #  local_obstacle_position = owner.current_position.to_local_space(owner.closest_obstacle.current_position)
         #   multipllier      = 1.0 + target.len()
         #   if target.len() != 0 : 
         #       multipllier -= local_obstacle_position.x / target.len()
        #    else:
         #       multipllier -= local_obstacle_position.x
        #    stering_force.x = (owner.closest_obstacle.RADIUS - local_obstacle_position.x) * 0.2
         #   stering_force.y = (owner.closest_obstacle.RADIUS - local_obstacle_position.y) * multipllier
            
        #    return owner.current_position.to_global_space(stering_force)
        return Vector(0,0)

    def seek(self, owner, target):
        s = (target- owner.current_position).norm() * owner.max_speed - owner.velocity * owner.priorities[0]
        seek_force = s
        
        #print(self.avoid(owner,target) * owner.priorities[1] )

        seek_force += self.avoid(owner,target) * owner.priorities[1]


       # seek_force = seek_force.trunc(s)
        return seek_force

    def arrival(self, owner, target):
        distance = target.distance_to(owner.current_position)
        avoid    = self.avoid(owner, target)
        velocity =  (target- owner.current_position).norm() * owner.max_speed     
        
      #  if owner.closest_obstacle != None:
      #      print(self.avoid(owner,target) * owner.priorities[1], velocity )

        return velocity + avoid - owner.velocity

    def execute(self, owner, player):
        owner.velocity = self.arrival(owner, player.current_position)/owner.m + owner.velocity
        distance       = player.current_position.distance_to(owner.current_position)

    #    if abs(owner.velocity.x) > owner.max_speed.x: owner.velocity.x = sign(owner.velocity.x) * owner.max_speed.x
    #    if abs(owner.velocity.y) > owner.max_speed.y: owner.velocity.y = sign(owner.velocity.y) * owner.max_speed.y

        owner.velocity = owner.velocity.trunc(owner.max_speed)
       # print( owner.closest_obstacle)
        if distance.len() < 20:
            owner.ai.change_state(FleeState())


