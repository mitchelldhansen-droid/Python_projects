import random

from data.player_stats import CLASS_STATS, CLASSES
from data.spell_stats import BASE_SPELL_SLOTS, CLASS_SPELLS
from items import Inventory
from signals import Signal


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
        self.max_spell_slots = BASE_SPELL_SLOTS[player_class] + (self.magic // 10)
        self.current_spell_slots = self.max_spell_slots
        self.active_buffs = {}
        self.damaged = Signal()
        self.healed = Signal()
        self.died = Signal()

    def display(self):
        print(" ")
        print("===  CHARACTER CREATED  ===")
        print(f"Name: {self.name}")
        print(f"Class: {self.player_class}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Attack: {self.attack_power}")
        print(f"Magic: {self.magic}")
        print(f"Spell Slots: {self.current_spell_slots}/{self.max_spell_slots}")
        print("===========================")

    def __str__(self):
        return f"{self.name} the {self.player_class}"

    def take_damage(self, damage):
        self.health -= damage
        self.damaged.emit(self, damage)
        if self.health <= 0:
            self.health = 0
            self.died.emit(self)
            return "died"
        else:
            return "damaged"

    def heal(self, amount):
        actual_heal = min(amount, self.max_health - self.health)
        self.health += actual_heal
        self.healed.emit(self, actual_heal)
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
        self.max_spell_slots = self._calculate_max_slots()
        self.current_spell_slots = self.max_spell_slots
        print(f"{self.name} has leveled up to level {self.level}!")
        print("+5 TO ALL STATS | +15 MAX HEALTH")
        print(
            f"Attack: {self.attack_power} | Magic: {self.magic} | Max Health: {self.max_health}"
        )

    def restore_spell_slots(self):
        self.current_spell_slots = self.max_spell_slots

    def use_spell_slots(self, amount):
        self.current_spell_slots -= amount

    def get_available_spells(self):
        return CLASS_SPELLS[self.player_class]

    def can_cast(self, spell_key):
        spell = CLASS_SPELLS[self.player_class][spell_key]
        slots_required = spell["slots_required"]
        if self.current_spell_slots >= slots_required:
            return True
        else:
            return False

    def _calculate_max_slots(self):
        return BASE_SPELL_SLOTS[self.player_class] + (self.magic // 10)

    def to_dict(self):
        return {
            "name": self.name,
            "player_class": self.player_class,
            "level": self.level,
            "attack_power": self.attack_power,
            "magic": self.magic,
            "health": self.health,
            "max_health": self.max_health,
            "max_spell_slots": self.max_spell_slots,
            "current_spell_slots": self.current_spell_slots,
            "has_companion": self.has_companion,
            "path_taken": self.path_taken,
            "inventory": self.inventory.items,
        }

    @classmethod
    def from_dict(cls, data):
        character = cls(data["name"], data["player_class"])
        character.level = data["level"]
        character.attack_power = data["attack_power"]
        character.magic = data["magic"]
        character.health = data["health"]
        character.max_health = data["max_health"]
        character.max_spell_slots = data["max_spell_slots"]
        character.current_spell_slots = data["current_spell_slots"]
        character.has_companion = data["has_companion"]
        character.path_taken = data["path_taken"]
        character.inventory.items = data["inventory"]
        return character


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
