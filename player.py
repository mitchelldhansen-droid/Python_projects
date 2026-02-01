import random

from data.player_stats import CLASS_STATS, CLASSES
from items import Inventory


class Character:
    def __init__(self, name, player_class):
        self.name = name
        self.player_class = player_class
        self.health = CLASS_STATS[player_class]["Health"]
        self.max_health = CLASS_STATS[player_class]["Health"]
        self.attack_power = CLASS_STATS[player_class]["Attack"]
        self.magic = CLASS_STATS[player_class]["Magic"]
        self.inventory = Inventory()
        self.level = 1
        self.has_companion = False
        self.path_taken = None

    def display(self):
        print(" ")
        print("===  CHARACTER CREATED  ===")
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")
        print("===========================")

    def __str__(self):
        return f"{self.name} the {self.player_class}"

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"{self.name} has been defeated!")
            return "died"
        else:
            print(f"{self.name} has taken {damage} damage.")
            print(f"Health is now: {self.health}")
            return "damaged"

    def heal(self, amount):
        actual_heal = min(amount, self.max_health - self.health)
        self.health += actual_heal
        print(f"{self.name} has been healed for {actual_heal} health.")
        return "healed"

    def defend(self, damage):
        reduced_damage = damage // 2
        print(f"{self.name} defends!")
        return self.take_damage(reduced_damage)

    def attack(self, target):
        damage = self.attack_power
        print(f"{self.name} attacks {target.name}!")
        return target.take_damage(damage)

    def use_potion(self):
        if self.inventory.has_item("Health Potion"):
            self.inventory.remove_item("Health Potion")
            heal_amount = random.randint(20, 25)
            self.heal(heal_amount)
            print(
                f"{self.name} drinks a health potion and heals for {heal_amount} health!"
            )
            return "healed"
        else:
            print(f"{self.name} has no health potions left!")
            return "no_potion"

    def level_up(self):
        self.level += 1
        self.max_health += 15
        self.health = self.max_health
        self.attack_power += 5
        self.magic += 5
        print(f"{self.name} has leveled up to level {self.level}!")
        print("+5 TO ALL STATS | +15 MAX HEALTH")
        print(
            f"Attack: {self.attack_power} | Magic: {self.magic} | Max Health: {self.max_health}"
        )


def create_character():
    name = input("What is your character's name?")
    print("Welcome," + name + "!")
    print("Choose your class:")
    for index, class_name in enumerate(CLASSES, start=1):
        print(f"{index}. {class_name}")
    while True:
        choice = input("Enter 1, 2, 3, or 4: ")
        if choice in ["1", "2", "3", "4"]:
            break
        else:
            print("Invalid choice. Please enter 1,2,3, or 4 to continue.")
    player_class = CLASSES[int(choice) - 1]
    print(name + " the " + player_class + "!")

    character = Character(name, player_class)

    return character
