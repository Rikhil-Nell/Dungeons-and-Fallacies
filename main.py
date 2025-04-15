# main.py
# This is the main entry point to run your game.
from game import play_game
# import asyncio # Uncomment if using async version

if __name__ == "__main__":
    # If using sync agent calls (as shown in game_logic.py):
    play_game()

    # If you switch game_logic.py to use async/await:
    # asyncio.run(play_game())