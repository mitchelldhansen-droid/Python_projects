import random

from player import player_defend, use_potion
from utils import spawn_enemy


def player_attack(enemy_health, attack_power, enemy_name):
    enemy_health -= attack_power
    print(f"The {enemy_name} takes {attack_power} damage!")
    return enemy_health


def enemy_damage(current_health, enemy_attack):
    damage_taken = enemy_attack
    current_health -= damage_taken
    print(f"You take {damage_taken} damage!")
    return current_health


def combat(enemy_name, enemy_health, enemy_attack, character, inventory, depth=0):
    print(f"a {enemy_name} appears! Health: {enemy_health}")
    while enemy_health > 0 and character["Health"] > 0:
        skip_enemy_turn = False
        print(f"Your Health: {character['Health']} | Enemy Health: {enemy_health}")
        print(f"Potions Remaining: {inventory['Health Potion']}")
        print("What do you do??")
        print("1. Attack")
        print("2. Defend")
        print("3. Drink Potion")

        action = input("Choose 1., 2., or 3.")

        if action == "1":
            print(f"You attack the {enemy_name}!")
            enemy_health = player_attack(enemy_health, character["Attack"], enemy_name)
            print(f"{enemy_name} Health is now: {enemy_health}")
        elif action == "2":
            print(f"You defend against the {enemy_name}'s attack!")
            character["Health"] = player_defend(enemy_attack, character["Health"])
            print(f"Health is now: {character['Health']}")
            skip_enemy_turn = True
        elif action == "3":
            character["Health"], inventory, used = use_potion(
                character["Health"], character["Max_Health"], inventory
            )
            if not used:
                continue
        else:
            print("Invalid action")
            continue
        if enemy_health <= 0:
            print(f"You defeated the {enemy_name}!")
            roll = random.random()
            if roll < 0.6:
                inventory["Health Potion"] += 1
                print(f"The {enemy_name} dropped a health potion! Added to inventory.")
            elif roll < 0.9:
                if depth < 1:
                    print("A skeleton clambors to life and attacks!")
                    skeleton_health, skeleton_attack = spawn_enemy("skeleton")
                    combat(
                        "skeleton",
                        skeleton_health,
                        skeleton_attack,
                        character,
                        inventory,
                        depth + 1,
                    )
            else:
                print(f"The {enemy_name} had nothing useful..")
        elif character["Health"] <= 0:
            print(f"You were defeated by the {enemy_name}!")
            print("GAME OVER")
            exit()
        elif not skip_enemy_turn:
            print(f"The {enemy_name} attacks!")
            character["Health"] = enemy_damage(character["Health"], enemy_attack)
            print(f"Health is now: {character['Health']}")


def pixie_encounter(character, inventory):
    print(
        "You exit the forest with your newly gained strength and come upon an idyllic glade."
    )
    print(
        "At least it seems idyllic, but you can't get rid of a thought that something is not what it seems."
    )
    print(
        "Like a worm drilling it's way out of an apple, the thought consumes your mind."
    )
    print(
        "Then suddenly, something flies at you faster than anything you've seen thus far and stops just short of your face."
    )
    print("A pixie appears. It shimmers in front of you, and begins to speak.")
    print(
        "Hello, brave adventurer! I see you have a lot of strength, did you happen to have something to trade?"
    )
    print(
        "I'm looking for something shiny and quite pointy, would you have anything like that?"
    )
    # check if player has knife
    if inventory["Knife"] > 0:
        # show trade or attack options
        print("You have a knife!")
        print("1. Trade")
        print("2. Attack")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("You trade your knife for a health potion.")
            inventory["Knife"] -= 1
            inventory["Health Potion"] += 1
            print(
                "The pixie is satisfied with your trade and smiles, and you notice she has tiny little daggers as teeth."
            )
            print("She inserts the dagger into her mouth, waves, and flies away.")
            print(
                "You have the feeling nothing here is going to make sense, and that you just avoided a difficult encounter."
            )
        elif choice == "2":
            print("You attack the pixie with your knife.")
            pixie_health, pixie_attack = spawn_enemy("pixie")
            original_health = pixie_health
            pixie_health = player_attack(pixie_health, character["Attack"], "pixie")
            print(f"Health is now: {character['Health']}")
            combat("pixie", pixie_health, pixie_attack, character, inventory, depth=0)
            if character["Health"] > 0:
                print("The pixie reforms somehow!")
                combat(
                    "pixie",
                    original_health // 2,
                    pixie_attack,
                    character,
                    inventory,
                    depth=1,
                )
                if character["Health"] > 0:
                    print(
                        "The pixie finally dissolves in a burst of light! You are victorious!"
                    )
                    inventory["Gold"] += 10
                    inventory["Health Potion"] += 2
                else:
                    print("You have been defeated by the pixie!")
                    print("GAME OVER")
                    exit()
            else:
                print("You have been defeated by the pixie!")
                print("GAME OVER")
                exit()
        else:
            print("Invalid choice.")
    elif inventory["Knife"] == 0:
        # show lie or attack options
        print("You don't have a knife.")
        print("1. Lie")
        print("2. Attack")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("You lie to the pixie.")
            print("The pixie is not convinced.")
            print("You dare deceive me?")
            print("She lunges at you with unnatural speed!")
            pixie_health, pixie_attack = spawn_enemy("pixie")
            original_health = pixie_health
            combat("pixie", pixie_health, pixie_attack, character, inventory, depth=0)
            if character["Health"] > 0:
                print("The pixie reforms somehow!")
                combat(
                    "pixie",
                    original_health // 2,
                    pixie_attack,
                    character,
                    inventory,
                    depth=1,
                )
                if character["Health"] > 0:
                    print(
                        "The pixie finally dissolves in a burst of light! You are victorious!"
                    )
                    inventory["Gold"] += 10
                    inventory["Health Potion"] += 2
                else:
                    print("You have been defeated!")
                    print("GAME OVER")
                    exit()
        elif choice == "2":
            print("You attack the pixie.")
            pixie_health, pixie_attack = spawn_enemy("pixie")
            original_health = pixie_health
            pixie_health = player_attack(pixie_health, character["Attack"], "pixie")
            print(f"Health is now: {character['Health']}")
            combat("pixie", pixie_health, pixie_attack, character, inventory, depth=0)
            if character["Health"] > 0:
                print("The pixie reforms somehow!")
                combat(
                    "pixie",
                    original_health // 2,
                    pixie_attack,
                    character,
                    inventory,
                    depth=1,
                )
                if character["Health"] > 0:
                    print(
                        "The pixie finally dissolves in a burst of light! You are victorious!"
                    )
                    inventory["Gold"] += 10
                    inventory["Health Potion"] += 2
                else:
                    print("You have been defeated!")
                    print("GAME OVER")
                    exit()
        else:
            print("Invalid choice.")
