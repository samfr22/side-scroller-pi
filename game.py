"""
Holds information about current game information and handles when to update the
game state
"""

from asteroid import Asteroid
import player

# Import sense hat
# Import sunfounder modules

class Game:
    """
    Handles all of the game state information and runs the logic to determine
    when to start, update, or end the game
    """
    asteroids
    display
    potentiometer
    temperature
    score = 0

    def __init__(self):
        """
        Initializes al of the game structures necessary and prepares the game to be run
        """
        player.reset()
        asteroids = []

        # TODO: Set up sensors via GPIO
        
        # TODO: Set up display with SenseHat

    def play(self):
        """
        The main loop of the game
        """


    def collision_detection(self):
        """
        Handles checking the position of the player against the position of any
        asteroids or the edges of the screen
        """
