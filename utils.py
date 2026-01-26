import random

from data.enemy_stats import ENEMY_STATS


def spawn_enemy(enemy_name):
    enemy_health = random.randint(*ENEMY_STATS[enemy_name]["health"])
    enemy_attack = random.randint(*ENEMY_STATS[enemy_name]["attack"])
    return enemy_health, enemy_attack


def game_over(character):
    print("GAME OVER" + " " + character["Name"] + "!")
    print("1. Restart")
    print("2. Quit")
    choice = input("Enter your choice: ")
    if choice == "1":
        return "restart"
    elif choice == "2":
        return "quit"
    else:
        print("Invalid choice")
        return game_over(character)
