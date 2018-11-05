from random import randint, uniform
from vector import Vector

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

        if owner.current_position.distance_to(player.current_position).len() < 200:
            owner.ai.change_state(SeekState())

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



class WanderState(State):
    state  = "Wander"
    
    def enter(self, owner):
        pass

    def exit(self, owner):
        pass

    def execute(self, owner, player):
        pass

class SeekState(State):
    state = "Seek"

    def enter(self, owner):
        pass

    def exit(self, owner):
        pass

    def seek(self, owner, target):
        seek_force =  (target- owner.current_position).norm() * owner.max_speed - owner.velocity
        return seek_force

    def arrival(self, owner, target):
        distance = target.distance_to(owner.current_position)
        velocity =  (target- owner.current_position).norm() * owner.max_speed     - owner.velocity
        return min( velocity , distance ) 

    def execute(self, owner, player):
        owner.velocity = self.arrival(owner, player.current_position)/owner.m + owner.velocity
        distance       = player.current_position.distance_to(owner.current_position)

    #    if abs(owner.velocity.x) > owner.max_speed.x: owner.velocity.x = sign(owner.velocity.x) * owner.max_speed.x
    #    if abs(owner.velocity.y) > owner.max_speed.y: owner.velocity.y = sign(owner.velocity.y) * owner.max_speed.y

        owner.velocity = owner.velocity.trunc(owner.max_speed)

        if distance.len() < 20:
            owner.ai.change_state(FleeState())


class PursitState(State):
    state = "Pursit"

    def enter(self, owner):
        pass

    def exit(self, owner):
        pass

    def execute(self, owner, player):

        distance = owner.current_position.distance_to(player.current_position)
        owner.velocity =  (player.current_position - owner.current_position).norm() * owner.max_speed     - owner.velocity

        owner.velocity = owner.velocity.trunc(owner.max_speed)

        if distance.len() < 30:
            owner.ai.change_state(FleeState())

def sign(x):
    return 1 if x > 0 else 0 if x == 0 else -1 

class FleeState(State):
    state = "Flee"

    def enter(self, owner):
        pass

    def exit(self, owner):
        pass

    def execute(self, owner, player):
        owner.velocity =  (( ( owner.current_position - player.current_position).norm() * owner.max_speed  - owner.velocity )/owner.m ) + owner.velocity

        owner.velocity = owner.velocity.trunc(owner.max_speed)
        
        distance = owner.current_position.distance_to(player.current_position)

        if distance.len() > 300:
            owner.ai.change_state(SeekState())
