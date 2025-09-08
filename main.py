from game import Game
import sys
from highscores import Highscores


if __name__ == '__main__':
    # Make a game instance, and run the game.
    game = Game()
    game.run()

    Highscores.update(game.level.player_name,game.level.ship.score)
    
    print("The game is over, thank you for playing.")

    sys.exit()