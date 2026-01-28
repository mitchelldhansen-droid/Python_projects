import random

from data.enemy_stats import ENEMY_STATS


class Enemy:
    def __init__(self, enemy_type):
        self.name = enemy_type
        self.health = random.randint(*ENEMY_STATS[enemy_type]["health"])
        self.attack_power = random.randint(*ENEMY_STATS[enemy_type]["attack"])

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"{self.name} has been defeated!!")
            return "died"
        else:
            print(f"{self.name} has taken {damage} damage.")
            return "damaged"

    def attack(self, target):
        damage = random.randint(self.attack_power - 3, self.attack_power + 3)
        print(f"the {self.name} attacks!")
        return target.take_damage(damage)
