from game import Game
import sys
from highscores import Highscores


if __name__ == '__main__':
    # Make a game instance, and run the game.
    game = Game()
    game.run()

    if Highscores.player_name is None:
        Highscores.update(game.level.ship.score)
    print(Highscores.new_highscore)
    print("The game is over, thank you for playing.")

    sys.exit()