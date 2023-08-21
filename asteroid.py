"""
OO Programming and Data Structures | CS 241
Asteroids Project 
Implemented by Von Brauner Medeiros de Souza
Spring 2021
This program implements the asteroids game.

File: asteroid.py
"""

import arcade
from flying_object import Flying_object
import random


ASTEROID_SAFE_RADIUS = 30
ALPHA = 255 # For transparency, 1 means not transparent

BIG_ASTEROID_SPIN = 1
MED_ASTEROID_SPIN = -2
SMALL_ASTEROID_SPIN = 5

ASTEROID_RADIUS = 30  #For collision detection, you can assume the ship is a circle of radius 30
MED_ASTEROID_RADIUS = 5 #MEdium: For collision detection, can be treated as a circle with radius 5
SMALL_ASTEROID_RADIUS = 2 #Small: For collision detection, can be treated as a circle with radius 2

class Asteroid(Flying_object):
    def __init__(self, start_x, start_y):
        super().__init__()
        self.center.x = start_x
        self.center.y = start_y
        self.velocity.dx = random.uniform(-2,1.5)  
        self.velocity.dy = random.uniform(-1.5,2) 

    def play_sound_asteroid_dead(self):
        self.asteroid_sound = arcade.load_sound("sounds/asteroid_dead_sound.mp3") 
        arcade.play_sound(self.asteroid_sound)

class Big_Asteroid(Asteroid):
    """ The Big Asteroid Class """
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.radius = ASTEROID_RADIUS

    def advance(self):
        super().advance()
        self.angle += BIG_ASTEROID_SPIN

    def draw(self):
        img = "images/meteorGrey_big1.png"
        texture = arcade.load_texture(img)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, 
                        texture.width, texture.height, texture, self.angle, ALPHA) 

class Med_Asteroid(Asteroid):
    """ The Medium Asteroid Class """
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.radius = MED_ASTEROID_RADIUS

    def advance(self):
        super().advance()
        self.angle += MED_ASTEROID_SPIN
  
    def draw(self):
        img = "images/meteorGrey_med1.png"
        texture = arcade.load_texture(img)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width, texture.height, texture, self.angle, ALPHA)    

class Small_Asteroid(Asteroid):
    """ The Small ASteroid Class """
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.radius = SMALL_ASTEROID_RADIUS

    def advance(self):
        super().advance()
        self.angle += SMALL_ASTEROID_SPIN

    def draw(self):
        img = "images/meteorGrey_small1.png"
        texture = arcade.load_texture(img)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width, texture.height, texture, self.angle, ALPHA)     
