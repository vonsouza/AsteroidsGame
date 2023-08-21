"""
OO Programming and Data Structures | CS 241
Asteroids Project 
Implemented by Von Brauner Medeiros de Souza
Spring 2021
This program implements the asteroids game.

File: ship.py
"""
import arcade
from flying_object import Flying_object
import math

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

SHIP_WIDTH = 50
SHIP_HEIGHT = 45

SHIP_SPEED = 3
SHIP_START_ANGLE = 45

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ALPHA = 255 # For transparency, 1 means not transparent

class Ship(Flying_object):
    """     The Ship     """ 
    def __init__(self):
        super().__init__()
        #Starting the Ship in the center of the screen
        self.center.x = SCREEN_WIDTH /2 
        self.center.y = SCREEN_HEIGHT /2
        self.radius = SHIP_RADIUS
        self.angle = SHIP_START_ANGLE

    def draw(self):
        img = "images/playerShip1_orange.png"
        texture = arcade.load_texture(img)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width, texture.height, texture, self.angle, ALPHA) 

    def play_sound_ship_dead(self):
        self.ship_sound = arcade.load_sound("sounds/ship_dead_sound.mp3") 
        arcade.play_sound(self.ship_sound)

    def move_right(self):
        self.angle -= SHIP_TURN_AMOUNT

    def move_left(self):
        self.angle += SHIP_TURN_AMOUNT

    def thrust(self):
        self.velocity.dx -= math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT      
        self.velocity.dy += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    def plunge(self):
        self.velocity.dx += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT      
        self.velocity.dy -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT 