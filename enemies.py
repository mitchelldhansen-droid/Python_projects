import random

from data.enemy_stats import ENEMY_STATS
from signals import Signal


class Enemy:
    def __init__(self, enemy_type):
        self.name = enemy_type.replace("_", " ").title()
        self.health = random.randint(*ENEMY_STATS[enemy_type]["health"])
        self.attack_power = random.randint(*ENEMY_STATS[enemy_type]["attack"])
        self.damaged = Signal()
        self.died = Signal()

    def take_damage(self, damage):
        self.health -= damage
        self.damaged.emit(self, damage)
        if self.health <= 0:
            self.health = 0
            self.died.emit(self)
            return "died"
        else:
            return "damaged"

    def attack(self, target):
        damage = random.randint(self.attack_power - 3, self.attack_power + 3)
        print(f"the {self.name} attacks!")
        return target.take_damage(damage)
