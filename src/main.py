from game.game import Game
import os
import sys


resolution = (900, 600)
# Forcer le répertoire courant à celui du script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    Game(resolution)