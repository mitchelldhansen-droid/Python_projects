import random

from player import player_defend, use_potion


def player_attack(enemy_health, attack_power, enemy_name):
    enemy_health -= attack_power
    print(f"The {enemy_name} takes {attack_power} damage!")
    return enemy_health


def enemy_damage(current_health):
    damage_taken = random.randint(5, 10)
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
                    skeleton_health = random.randint(20, 35)
                    skeleton_attack = random.randint(4, 8)
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
        elif not skip_enemy_turn:
            print(f"The {enemy_name} attacks!")
            character["Health"] = enemy_damage(character["Health"])
            print(f"Health is now: {character['Health']}")
