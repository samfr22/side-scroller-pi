"""
Main File -> Entry point
"""

from game import Game

def main():
    game = Game()
    print("Game setup, starting game...")
    game.play()

if __name__ == "__main__":
    main()
