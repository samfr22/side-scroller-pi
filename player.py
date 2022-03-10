# Import library for handling the joystick

class Player:
    """
    Handles the data for the player and handles their movement
    """

    pos_x = 0
    pos_y = 4
    num_lives = 4
    
    def move(self):
        """
        Method to handle the player's movement of the joystick and update their
        position accordingly to the game
        """
