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
        position accordingly to the game
        """
        vert_reading = ADC.read(0)
        if vert_reading <= 30 and self.pos_y > 0:
            # Up
            self.pos_y -= 1
            print("Up")
        elif vert_reading >= 225 and self.pos_y < 7:
            # Down
            self.pos_y += 1
            print("Down")
        hoz_reading = ADC.read(1)
        if hoz_reading >= 225 and self.pos_x > 0:
            # Left
            self.pos_x -= 1
            print("Left")
        elif hoz_reading <= 30 and self.pos_x < 7:
            # Right
            self.pos_x += 1
            print("Right")

        pressed = ADC.read(2)
        if pressed <= 30:
            # TODO: Shooting mechanic?
            pass
        
        return (self.pos_x, self.pos_y)