"""
Holds information about current game information and handles when to update the
game state
"""

# TODO: Import sense hat
import PCF8591 as ADC
import LCD1602 as LCD
from asteroid import Asteroid
from player import Player
import time
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
    ASTEROID_BASE_GEN_SPEED = 3
    BASE_SCORE_MULTIPLIER = 0.01
    # How many times the game loops per second
    LOOP_RATE = 20

    def __init__(self):
        """
        Initializes all of the game structures necessary and prepares the game to be run
        """
        self.asteroids = []

        # Set up sensors and displays
        ADC.setup(0x48)
        LCD.init(0x27, 1)
        LCD.clear()
        
        # TODO: Set up display with SenseHat

    def play(self):
        """
        The main loop of the game
        """
        score_multiplier = self.BASE_SCORE_MULTIPLIER
        # Time until the next asteroid comes in
        next_asteroid_time = self.ASTEROID_BASE_GEN_SPEED * self.LOOP_RATE
        asteroid_gen_speed_decrease = 0.0
        next_asteroid = 0
        # Time since last asteroid pos update (update once a second)
        last_asteroid_update = 0
        
        last_pos = (0, 0)

        while True:
            # Get sensor inputs
            potentiometer_reading = ADC.read(3)
            output1 = "Val: %s" % (potentiometer_reading,)
            LCD.write(0, 1, output1)

            # Update positions of player and asteroids
            player_pos = self.player.move()
            if last_pos[0] != player_pos[0] or last_pos[1] != player_pos[1]:
                self.display[last_pos[0]][last_pos[1]] = '_'
                last_pos = player_pos
                self.display[player_pos[0]][player_pos[1]] = 'X'

            print("Pos: %s, %s" % (player_pos[0], player_pos[1]))

            last_asteroid_update += 1
            if last_asteroid_update >= self.LOOP_RATE:
                last_asteroid_update = 0

                for asteroid in self.asteroids:
                    updated = asteroid.update_pos()
                    if updated[0] < 0:
                        self.asteroids.remove(asteroid)
                        self.display[0][updated[1]] = '_'
                    else:
                        print("Asteroid at %s, %s" % (updated[0], updated[1]))
                        self.display[updated[0]][updated[1]] = 'A'
                        self.display[updated[0] + 1][updated[1]] = '_'

            self.print_display()

            if self.collision_detection():
                # Collision detected - lose a life and reset to original position
                self.player.pos_x = 0
                self.player.pos_y = 4
                score_multiplier = self.BASE_SCORE_MULTIPLIER
                self.player.num_lives -= 1
                if self.player.num_lives <= 0:
                    # Game over
                    LCD.write(0, 1, "Game over!")
                    exit(0)

            # Check if time to generate a new asteroid
            next_asteroid += 1
            if next_asteroid >= next_asteroid_time:
                score_multiplier += 0.01
                next_asteroid = 0
                asteroid_gen_speed_decrease += 0.05
                next_asteroid_time = (self.ASTEROID_BASE_GEN_SPEED - asteroid_gen_speed_decrease) * self.LOOP_RATE

                self.asteroids.append(Asteroid(random.randint(0, 7)))

            # Update score
            self.score += (self.score * score_multiplier)
            LCD.write(0, 0, ("Score: %s" % (str(math.floor(self.score)))))

            time.sleep(1 / self.LOOP_RATE)


    def collision_detection(self):
        """
        Handles checking the position of the player against the position of any
        asteroids or the edges of the screen
        """
        for asteroid in self.asteroids:
            if asteroid.pos_x == self.player.pos_x and asteroid.pos_y == self.player.pos_y:
                # Collision - remove the asteroid
                self.display[asteroid.pos_x][asteroid.pos_y] = '_'
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
