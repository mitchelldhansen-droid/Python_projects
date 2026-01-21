import random

from data.enemy_stats import ENEMY_STATS


def spawn_enemy(enemy_name):
    enemy_health = random.randint(*ENEMY_STATS[enemy_name]["health"])
    enemy_attack = random.randint(*ENEMY_STATS[enemy_name]["attack"])
    return enemy_health, enemy_attack
