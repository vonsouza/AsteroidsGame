"""
OO Programming and Data Structures | CS 241
Asteroids Project 
Implemented by Von Brauner Medeiros de Souza
Spring 2021
This program implements the asteroids game.

File: little_ship.py
"""
import arcade
from point import Point

ALPHA = 255 # For transparency, 1 means not transparent

class Little_Ship():
    """     The Little Ship that represents the lives    """ 
    def __init__(self, x, y):
        self.center = Point()
        self.center.x = x #SCREEN_WIDTH - 780
        self.center.y = y #SCREEN_HEIGHT - 20

    def draw(self):
        img = "images/playerShip1_orange.png"
        texture = arcade.load_texture(img)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width -60, texture.height-40, texture, 0, ALPHA) 
