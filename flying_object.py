"""
OO Programming and Data Structures | CS 241
Asteroids Project 
Implemented by Von Brauner Medeiros de Souza
Spring 2021
This program implements the asteroids game.

File: flying_object.py
"""

from point import Point
from velocity import Velocity
from abc import ABC

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Flying_object(ABC):
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0
        self.alive = True
        self.angle = 0
            
    def advance(self):
        # Checking wrapping
        self.check_wrap()
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def hit(self):
        self.alive = False 

    def draw(self):
        pass

    def check_wrap(self):
        """Checks to see if the flying object (asteroid, ship or bullet) has hit the borders
        of the screen and if so, wrap"""
        if self.center.x < 0 :
            self.center.x +=  SCREEN_WIDTH
        if self.center.x > SCREEN_WIDTH : 
            self.center.x -=  SCREEN_WIDTH
        if self.center.y < 0 :
            self.center.y += SCREEN_HEIGHT
        if self.center.y > SCREEN_HEIGHT :
            self.center.y -= SCREEN_HEIGHT
