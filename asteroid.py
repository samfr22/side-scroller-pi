class Asteroid:
    """
    Handles the data for an asteroid
    """

    def __init__(self, pos_y):
        self.pos_y = pos_y
        self.pos_x = 7

    def update_pos(self):
        """
        Moves the asteroids one column over on the game screen and returns the
        new position to the game class
        """

        self.pos_x -= 1

        return (self.pos_x, self.pos_y)
