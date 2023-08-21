"""
OO Programming and Data Structures | CS 241
Asteroids Project 
Implemented by Von Brauner Medeiros de Souza
Spring 2021
This program implements the asteroids game.

File: game.py
"""
import arcade
import random

from little_ship import Little_Ship
from ship import Ship
from asteroid import Big_Asteroid, Med_Asteroid, Small_Asteroid
from bullet import Bullet

from arcade.color import MEDIUM_AQUAMARINE
from pyglet.libs.win32.constants import FALSE, TRUE

# These are Global constants to use throughout the game
BACKGROUND_COLOR = arcade.color.SMOKY_BLACK
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BULLET_LIFE = 60
TOTAL_OF_ASTEROIDS = 35
LIVES_NUMBER = 3
DISTANCE_BETWEEN_LITTLE_SHIPS = 43
CICLES_WITHOUT_CHECK_COLLISIONS = 130

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of each of the above classes.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)     
        self.ship = Ship()        
        arcade.set_background_color(BACKGROUND_COLOR)
        self.held_keys = set()
        self.little_ships = []
        self.create_little_ships()  
        # 5 large asteroids appearing on the screen. List of asteroid
        self.asteroids = []
        self.create_initial_asteroids()
        #List of bullets
        self.bullets = []
        self.asteroids_killed = 0
        self.game_over = FALSE

        #After the ship is hit, it restarts. However, it needs some time without being hit.
        self.without_collisions = CICLES_WITHOUT_CHECK_COLLISIONS

    def create_little_ships(self):
        """The little ships (on on the up left) represent the number of lives remaining"""
        position_x = SCREEN_WIDTH - 780
        position_y = SCREEN_HEIGHT - 20
        i = 0
        while i < LIVES_NUMBER:
            little_ship = Little_Ship(position_x, position_y)
            self.little_ships.append(little_ship)
            position_x += DISTANCE_BETWEEN_LITTLE_SHIPS
            i +=1

    def create_initial_asteroids(self):
        """ Create 5 large asteroid initials in random places """
        i = 1
        while i <= 5:
            x = random.uniform(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
            y = random.uniform(SCREEN_WIDTH / 2, SCREEN_HEIGHT )
            asteroid = Big_Asteroid(x, y)
            self.asteroids.append(asteroid)
            i += 1

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()

        # Drawing each object
        self.ship.draw()

        for little in self.little_ships:
            little.draw()

        #bullets
        for bullet in self.bullets:
            bullet.draw()
        
        #asteroids
        for asteroid in self.asteroids:
            asteroid.draw()
     
        if self.game_over:
            arcade.start_render()
            arcade.set_background_color(arcade.color.WHITE)
            arcade.draw_text("GAME OVER",
                         (SCREEN_WIDTH // 2) - 170, SCREEN_HEIGHT // 2, arcade.color.BLACK, 50)
        
        if self.asteroids_killed >= TOTAL_OF_ASTEROIDS:
            arcade.start_render()
            arcade.set_background_color(arcade.color.WHITE)
            arcade.draw_text("YOU WON",
                         (SCREEN_WIDTH // 2) - 170, SCREEN_HEIGHT // 2, arcade.color.BLACK, 50)
        
    def update(self, delta_time):
        """ Update each object in the game. """
        self.check_keys()
        
        for asteroid in self.asteroids:
            asteroid.advance()

        for bullet in self.bullets:
            bullet.advance()
            bullet.frame += 1 

        self.ship.advance()

        # Checking collisions
        if self.without_collisions <= 0:
            #After the ship is hit, it restarts. However, it needs some time without being hit.
            self.check_collisions()
        else:
            self.without_collisions -= 1

    def check_collisions(self):
        """ Checks to see if there are collisions. """
        self.check_collisions_between_bullet_asterois()
        self.check_collisions_between_ship_asterois()

        # Checking for anything that is dead, and remove it
        self.cleanup_zombies()
        arcade.play_sound

    def check_collisions_between_bullet_asterois(self):
        """  Checking asteroids collision. Checking hits between Bullet and Asteroid """
        for bullet in self.bullets:
            #checking bullet hits asteroid
            for asteroid in self.asteroids:

                # Making sure they are both alive before checking for a collision
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    #Bullet hits asteroid
                    if (abs(bullet.center.x - asteroid.center.x) < too_close and
                                abs(bullet.center.y - asteroid.center.y) < too_close):
                        # its a hit!
                        bullet.hit() 
                        asteroid.hit() 
                        asteroid.play_sound_asteroid_dead()
                        self.asteroids_killed += 1              
                        
                        #Because the Bullet hits a asteroid, two asteroid must be created
                        self.break_asteroids(asteroid) 

    def check_collisions_between_ship_asterois(self):
        """  Checking Ship collision.Checking hits between Ship and Asteroid """
        for asteroid in self.asteroids:
            if asteroid.alive:
                too_close = self.ship.radius + asteroid.radius

                #asteroid hits ship
                if (abs(self.ship.center.x - asteroid.center.x) < too_close and
                    abs(self.ship.center.y - asteroid.center.y) < too_close):

                    self.ship.hit() 
                    self.ship.play_sound_ship_dead()
                    if len(self.little_ships) <= 0:
                        self.finish_game()
                    else:
                        #Restarting the Ship in the center of the screen
                        self.little_ships.pop()
                        self.restar_ship()

    def restar_ship(self):
        """The ship was hit. It starts the ship again."""
        self.without_collisions = CICLES_WITHOUT_CHECK_COLLISIONS #After the ship is hit, it restarts. However, it needs some time without being hit.
        self.ship = Ship()

    def break_asteroids(self, asteroid):
        """ 
        Receives an asteroid and breaks it in two
        If it's a big asteroid, it creates 2 medium asteroids
        If it's a medium asteroid, it creates 2 small asteroids
        """
        if type(asteroid) is Big_Asteroid:
            self.create_two_med_asteroids(asteroid)
        elif type(asteroid) is Med_Asteroid:
            self.create_two_small_asteroids(asteroid)

    def create_two_med_asteroids(self, asteroid):
        """ Creates 2 medium asteroids in the same place as the dead asteroid  """      
        med_asteroid1 = Med_Asteroid(asteroid.center.x, asteroid.center.y)
        med_asteroid2 = Med_Asteroid(asteroid.center.x, asteroid.center.y)

        self.asteroids.append(med_asteroid1) 
        self.asteroids.append(med_asteroid2) 

    def create_two_small_asteroids(self, asteroid):
        """ Creates 2 small asteroids in the same place as the dead asteroid  """   
        small_asteroid1 = Small_Asteroid(asteroid.center.x, asteroid.center.y)
        small_asteroid2 = Small_Asteroid(asteroid.center.x, asteroid.center.y)

        self.asteroids.append(small_asteroid1) 
        self.asteroids.append(small_asteroid2) 

    def cleanup_zombies(self):
        """ Removes any dead bullets or asteroids from the list."""
        for bullet in self.bullets:
            if not bullet.alive or bullet.frame >= BULLET_LIFE: #Bullets only live for 60 frames
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)

    def finish_game(self):
        """ Game finished. Empty the asteroids and bullets """
        self.game_over = TRUE
        self.bullets = []
        self.asteroids = []
 
    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.move_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.move_right()

        if arcade.key.UP in self.held_keys:
            self.ship.thrust()

        if arcade.key.DOWN in self.held_keys:
            self.ship.plunge()

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)
            if key == arcade.key.SPACE:
                bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y)
                self.bullets.append(bullet)
                bullet.fire() 
                bullet.play_sound_fire()

    def on_key_release(self, key: int, modifiers: int):
        """ Removes the current key from the set of held keys. """
        #keys
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = True

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = True

        if key in self.held_keys:
            self.held_keys.remove(key)

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()