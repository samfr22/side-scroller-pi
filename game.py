"""
Holds information about current game information and handles when to update the
game state
"""

import PCF8591 as ADC
import LCD1602 as LCD
import senseLED as LED
from asteroid import Asteroid
from player import Player
import random
import math

class Game:
    """
    Handles all of the game state information and runs the logic to determine
    when to start, update, or end the game
    """
    score = 1
    player = Player()
    display = [
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
    ]

    # Time at the beginning of the game to generate a new asteroid
    ASTEROID_BASE_GEN_SPEED = 2
    BASE_SCORE_MULTIPLIER = 0.5
    # How many times the game loops per second
    LOOP_RATE = 20
    player_color = (0, 0, 63)
    asteroid_color = (63, 0, 0)
    back_color = (0, 0, 0)

    def __init__(self):
        """
        Initializes all of the game structures necessary and prepares the game to be run
        """
        self.asteroids = []

        # Set up sensors and displays
        ADC.setup(0x48)
        LCD.init(0x27, 1)
        LCD.clear()
        LED.clear()

    def play(self):
        """
        The main loop of the game
        """
        score_multiplier = self.BASE_SCORE_MULTIPLIER
        potentiometer_mult = 0

        # Time until the next asteroid comes in
        next_asteroid_time = self.ASTEROID_BASE_GEN_SPEED * self.LOOP_RATE
        asteroid_gen_speed_decrease = 0.0
        next_asteroid = 0
        skip_update = False
        
        last_pos = (0, 0)
        last_potential = 0

        while True:
            # Get sensor input of potentiometer - speeds up game and scoring
            potentiometer_reading = ADC.read(3)
            if potentiometer_reading != last_potential:
                last_potential = potentiometer_reading
                potentiometer_mult = round(last_potential / 255, 1)

            output1 = "BM: %s Lives: %s" % (potentiometer_mult, self.player.num_lives)
            LCD.write(0, 1, output1)

            # Update positions of player and asteroids
            player_pos = self.player.move()
            if last_pos[0] != player_pos[0] or last_pos[1] != player_pos[1]:
                self.set_display_point(last_pos[0], last_pos[1], '_')
                last_pos = player_pos
                self.set_display_point(player_pos[0], player_pos[1], 'X')

            # self.print_display()
            LED.flush_pixels()

            if self.collision_detection():
                # Collision detected - lose a life and reset to original position
                self.player.pos_x = 0
                self.player.pos_y = 4
                self.set_display_point(0, 4, 'X')

                # Reset scoring information and slow asteroid generation speed
                score_multiplier = self.BASE_SCORE_MULTIPLIER
                next_asteroid_time = self.ASTEROID_BASE_GEN_SPEED * self.LOOP_RATE
                
                self.player.num_lives -= 1
                if self.player.num_lives <= 0:
                    # Game over
                    LCD.write(0, 1, "Game over!      ")
                    exit(0)

            # Check if time to generate a new asteroid
            next_asteroid += max(1, (potentiometer_mult * 10))
            if next_asteroid >= next_asteroid_time:
                if not skip_update:
                    # Update existing asteroids every other generation
                    for asteroid in self.asteroids:
                        updated = asteroid.update_pos()
                        # Check if out of the screen
                        if updated[0] < 0:
                            self.asteroids.remove(asteroid)
                            self.set_display_point(0, updated[1], '_')
                        else:
                            self.set_display_point(updated[0], updated[1], 'A')
                            self.set_display_point(updated[0] + 1, updated[1], '_')
                else:
                    skip_update = True

                score_multiplier += 0.01
                next_asteroid = 0
                asteroid_gen_speed_decrease += 0.01
                next_asteroid_time = (self.ASTEROID_BASE_GEN_SPEED - asteroid_gen_speed_decrease) * self.LOOP_RATE

                new_asteroid = Asteroid(random.randint(0, 7))
                self.set_display_point(new_asteroid.pos_x, new_asteroid.pos_y, 'A')
                self.asteroids.append(new_asteroid)

            # Update score
            self.score = self.score + (score_multiplier * potentiometer_mult)
            LCD.write(0, 0, ("Score: %s" % (str(math.floor(self.score)))))


    def collision_detection(self):
        """
        Handles checking the position of the player against the position of any
        asteroids or the edges of the screen
        """
        for asteroid in self.asteroids:
            if asteroid.pos_x == self.player.pos_x and asteroid.pos_y == self.player.pos_y:
                # Collision - remove the asteroid
                self.set_display_point(asteroid.pos_x, asteroid.pos_y, '_')
                self.asteroids.remove(asteroid)
                return True

        return False


    def print_display(self):
        """
        Debugging method while unable to use senseHAT at same time as inputs
        """
        for i in range(8):
            for j in range(8):
                print(self.display[j][i], end=" ")
            print()

    def set_display_point(self, x, y, marker):
        self.display[x][y] = marker
        if marker == '_':
            LED.set_pixel(x, y, self.back_color)
        elif marker == 'A':
            LED.set_pixel(x, y, self.asteroid_color)
        else:
            LED.set_pixel(x, y, self.player_color)
