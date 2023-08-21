import arcade
import math

from flying_object import Flying_object

BULLET_RADIUS = 30
BULLET_SPEED = 10
ALPHA = 255 # For transparency, 1 means not transparent

class Bullet(Flying_object):
    """The Small ASteroid Class"""
    def __init__(self, ship_angle, ship_x, ship_y):
        super().__init__()
        self.radius = BULLET_RADIUS

        #The Bullet starts on Ship location
        self.angle = ship_angle - 90
        self.center.x = ship_x
        self.center.y = ship_y

        #Bullets only live for 60 frames
        self.__frame = 0

        self.fire_sound = arcade.load_sound("sounds/fire_sound.mp3") 

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, val):
        if val < 0:
            self.__frame = 0
        elif val > 60:
            self.__frame = 60
        else:
            self.__frame = val

    def fire(self):
        self.velocity.dx -= math.sin(math.radians(self.angle +90)) * BULLET_SPEED      
        self.velocity.dy += math.cos(math.radians(self.angle +90)) * BULLET_SPEED 

    def play_sound_fire(self):
        arcade.play_sound(self.fire_sound)

    def draw(self):
        img = "images/laserBlue01.png"
        texture = arcade.load_texture(img)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width, texture.height, texture, self.angle, ALPHA) 