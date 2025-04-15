import os
import random

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_status(player_health, mob_name, mob_current_health):
    """Displays the current player and enemy health."""
    player_display_health = max(0, player_health)
    mob_display_health = max(0, mob_current_health)
    print("-" * 30)
    print(f"Player Health : {'❤️' * player_display_health}")
    print(f"Enemy: {mob_name} | Health: {'❤️' * mob_display_health}")
    print("-" * 30)

def roll_dice(sides=6):
    """Rolls a standard die."""
    return random.randint(1, sides)

