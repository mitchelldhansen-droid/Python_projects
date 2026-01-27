import random

from data.player_stats import CLASS_STATS, CLASSES


class Character:
    def __init__(self, name, player_class):
        self.name = name
        self.player_class = player_class
        self.health = CLASS_STATS[player_class]["Health"]
        self.max_health = CLASS_STATS[player_class]["Health"]
        self.attack_power = CLASS_STATS[player_class]["Attack"]
        self.magic = CLASS_STATS[player_class]["Magic"]
        self.inventory = {"Health Potion": 3, "Knife": 0, "Gold": 0}

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


def display_character(character):
    print(" ")
    print("===  CHARACTER CREATED  ===")
    for key, value in character.items():
        print(f"{key}: {value}")
    print("===========================")


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


def player_defend(wolf_attack, player_health):
    damage_taken = wolf_attack // 2
    player_health -= damage_taken
    print(f"You take {damage_taken} damage!")
    return player_health


def use_potion(current_health, max_health, inventory):
    heal_amount = random.randint(20, 25)
    if inventory["Health Potion"] > 0:
        inventory["Health Potion"] -= 1
        current_health += heal_amount
        if current_health > max_health:
            current_health = max_health
            print("You can't heal past max health!")
        print(f"You drink a health potion and heal for {heal_amount} health!")
        return current_health, inventory, True
    else:
        print("You have no health potions left!")
        return current_health, inventory, False
