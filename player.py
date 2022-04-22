"""
Handles the data for the player and handles their movement
"""

import PCF8591 as ADC

class Player:
    """
    Handles all of the information for the player
    """

    def __init__(self):
        """
        Initialize player information
        """
        self.pos_x = 0
        self.pos_y = 4
        self.num_lives = 4

    def move(self):
        """
        Method to handle the player's movement of the joystick and update their
        position accordingly to the game. Needs to be inverted in the vertical 
        posiition due to the behavior of the LED
        """
        vert_reading = ADC.read(0)
        if vert_reading <= 30 and self.pos_y < 7:
            # Down
            self.pos_y += 1
        elif vert_reading >= 225 and self.pos_y > 0:
            # Up
            self.pos_y -= 1
        hoz_reading = ADC.read(1)
        if hoz_reading >= 225 and self.pos_x > 0:
            # Left
            self.pos_x -= 1
        elif hoz_reading <= 30 and self.pos_x < 7:
            # Right
            self.pos_x += 1
        
        return (self.pos_x, self.pos_y)