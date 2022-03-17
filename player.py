# Import library for handling the joystick

"""
Handles the data for the player and handles their movement
"""

pos_x
pos_y
num_lives

def reset():
    """
    Sets the data of the module back to the default values for the beginning
    of the game
    """
    pos_x = 0
    pos_y = 4
    num_lives = 4

def move():
    """
    Method to handle the player's movement of the joystick and update their
    position accordingly to the game
    """
