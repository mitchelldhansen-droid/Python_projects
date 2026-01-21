import random

from data.player_stats import CLASS_STATS, CLASSES


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

    stats = CLASS_STATS[player_class]

    character = {
        "Name": name,
        "Class": player_class,
        "Health": stats["Health"],
        "Max_Health": stats["Health"],
        "Attack": stats["Attack"],
        "Magic": stats["Magic"],
    }

    inventory = {"Health Potion": 3, "Knife": 0, "Gold": 0}
    return character, inventory


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
