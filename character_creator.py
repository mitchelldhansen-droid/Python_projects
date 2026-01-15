# import json
import random

CLASSES = ["Warrior", "Mage", "Rogue", "Paladin"]
CLASS_STATS = {
    "Warrior": {"Health": 100, "attack": 15, "magic": 5},
    "Mage": {"Health": 60, "Attack": 5, "Magic": 20},
    "Rogue": {"Health": 75, "Attack": 12, "Magic": 8},
    "Paladin": {"Health": 85, "Attack": 10, "Magic": 12},
}


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

    inventory = {"Health Potion": 3, "Knife": 0}
    return character, inventory


character, inventory = create_character()


def display_character(character):
    print(" ")
    print("===  CHARACTER CREATED  ===")
    for key, value in character.items():
        print(f"{key}: {value}")
    print("===========================")


def player_attack(enemy_health, attack_power, enemy_name):
    enemy_health -= attack_power
    print(f"The {enemy_name} takes {attack_power} damage!")
    return enemy_health


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


display_character(character)

# Wolf stats
wolf_health = random.randint(30, 50)
wolf_attack = random.randint(5, 10)


def enemy_damage(current_health):
    damage_taken = random.randint(5, 10)
    current_health -= damage_taken
    print(f"You take {damage_taken} damage!")
    return current_health


def combat(enemy_name, enemy_health, enemy_attack, character, inventory, depth=0):
    print(f"a {enemy_name} appears! Health: {enemy_health}")
    while enemy_health > 0 and character["Health"] > 0:
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
        else:
            print(f"The {enemy_name} attacks!")
            character["Health"] = enemy_damage(character["Health"])
            print(f"Health is now: {character['Health']}")


def rest(character, inventory, is_dangerous=False):
    print("\nYou decide to take advantage of the nearly setup camp.")
    print("The fire pit is cold but there's dry wood stacked nearby.")

    if is_dangerous:
        roll = random.random()
        if roll < 0.5:
            # Owlbear ambush while resting!
            print("\nBut as you settle in, a massive shadow looms over you!")
            print("An Owlbear attacks!")
            print("You take 15 damage")
            character["Health"] = character["Health"] - 15
            owlbear_health = random.randint(40, 60)
            owlbear_attack = random.randint(8, 15)
            print("Health is now: " + str(character["Health"]))
            if character["Health"] <= 0:
                print("You were defeated by the Owlbear..")
                print("GAME OVER")
                return True  # Owlbear happened
            else:
                combat(
                    "Owlbear",
                    owlbear_health,
                    owlbear_attack,
                    character,
                    inventory,
                    depth=1,
                )
                # After Owlbear, continue with the rest
                print("\nAfter the brutal fight, you finally get your rest...")

    if character["Health"] < character["Max_Health"]:
        character["Health"] = character["Max_Health"]
        print("You rest by the rekindled fire. Health fully restored!")
    else:
        print("You're already at full health, but the rest is welcome.")

    inventory["Health Potion"] += 1
    print("Searching the camp, you find a health potion left behind.")

    print("\nCurrent Status:")
    print(f"Health: {character['Health']}/{character['Max_Health']}")
    print(f"Potions: {inventory['Health Potion']}")

    return False


def search(inventory, character, is_dangerous=False, depth=0):
    print("You decide to search around for any useful supplies")
    roll = random.random()
    if is_dangerous:
        # 50% Owlbear chance on dangerous search
        if roll < 0.5:
            print(
                "A large and menacing creature approaches with the head of an owl and the body of a bear!"
            )
            print("An Owlbear attacks!")
            print("You take 15 damage")
            character["Health"] = character["Health"] - 15
            owlbear_health = random.randint(40, 60)
            owlbear_attack = random.randint(8, 15)
            print("Health is now: " + str(character["Health"]))
            if character["Health"] <= 0:
                print("You were defeated by the Owlbear..")
                print("GAME OVER")
            else:
                combat(
                    "Owlbear",
                    owlbear_health,
                    owlbear_attack,
                    character,
                    inventory,
                    depth + 1,
                )
            return True  # Owlbear happened
        else:
            # 50% split between potion and knife
            if roll < 0.75:  # 0.5 to 0.75 = 25% of total = 50% of remaining
                print(
                    "You find another health potion! They must have left in a hurry..."
                )
                inventory["Health Potion"] += 1
            else:
                print("You find a small knife, it might come in handy.")
                inventory["Knife"] += 1
            return False  # No Owlbear
    else:
        if roll < 0.5:
            print("You find another health potion! They must have left in a hurry...")
            inventory["Health Potion"] += 1
            return False
        elif roll < 0.9:
            print("You find a small knife, it might come in handy.")
            inventory["Knife"] += 1
            return False
        else:
            print(
                "A large and menacing creature approaches with the head of an owl and the body of a bear!"
            )
            print("An Owlbear attacks!")
            print("You take 15 damage")
            character["Health"] = character["Health"] - 15
            # Owlbear stats
            owlbear_health = random.randint(40, 60)
            owlbear_attack = random.randint(8, 15)
            print("Health is now: " + str(character["Health"]))
            if character["Health"] <= 0:
                print("You were defeated by the Owlbear..")
                print("GAME OVER")
            else:
                combat(
                    "Owlbear",
                    owlbear_health,
                    owlbear_attack,
                    character,
                    inventory,
                    depth + 1,
                )
            return True  # Owlbear happened


def campsite_menu(character, inventory):
    has_rested = False
    has_searched = False
    while True:
        print("\n===Campsite===")
        print("What do you want to do?")
        if not has_rested:
            print("1. Rest and recover your health")
            if has_searched:
                print("   (WARNING: 50% chance of DANGEROUS encounter!)   ")
        if not has_searched:
            print("2. Search for more supplies")
            if has_rested:
                print("   (WARNING: 50% chance of DANGEROUS encounter!)   ")
        print("3. Push onward to the next challenge")
        choice = input(" Choose an option:")
        if choice == "1" and not has_rested:
            owlbear_happened = rest(character, inventory, is_dangerous=has_searched)
            has_rested = True
            if owlbear_happened:
                print("\nAfter that brutal fight, you must rest before continuing..")
                rest(character, inventory)
        elif choice == "2" and not has_searched:
            owlbear_happened = search(inventory, character, is_dangerous=has_rested)
            has_searched = True
            if owlbear_happened:
                print("\n After that brutal fight, you must rest before continuing..")
                rest(character, inventory)
                break
        elif choice == "3":
            break
        else:
            print("Invalid choice, select again.")
            continue
        if has_rested and has_searched:
            print("\n You've done what you can here, it's time to move on.")
            break


def boss_fight(character, inventory):
    print(
        "A massive behemoth made of bone and sinew emerges from, no, IS the twisted gnarled 'tree' you saw earlier."
    )
    print(
        "You look down at yourself and see that you're covered in blood, adventurers have long come here to die, it seems."
    )
    print(
        "Your heart races and your eyes dilate as you behold an unnatural abomination of a creature. A creature who now wants to absorb you."
    )
    boss_health = random.randint(70, 85)
    boss_attack = random.randint(15, 18)
    print(
        "You barely see it coming. A huge tentacle of absorbed flesh rends through the air cutting towards you."
    )
    character["Health"] -= 20
    print(f"Your Health: {character['Health']}/{character['Max_Health']}")
    if character["Health"] < 0:
        print("You didn't stand a chance")
        print("GAME OVER")
        exit()
    combat("Abomination", boss_health, boss_attack, character, inventory, depth=0)
    if character["Health"] > 0:
        print("\n" + "=" * 50)
        print("You emerge victorious, the Abomination's power absorbed into you.")
        print("You feel stronger, more resilient than ever before.")
        character["Attack"] += 5
        character["Magic"] += 5
        character["Max_Health"] += 15
        character["Health"] = character["Max_Health"]
        print("+5 TO ALL STATS | +15 MAX HEALTH")
        print(
            f"Attack: {character['Attack']} | Magic: {character['Magic']} | Max Health: {character['Max_Health']}"
        )
        print("Level Up!")
        print("VICTORY!")
        print("\n" + "=" * 50)


print(" ")
print(
    "You hear a growling, and leaves rustle as something lifts off from the forest floor and the shape of a wolf lunges towards you! You take 10 damage"
)
character["Health"] = character["Health"] - 10
print("Health is now: " + str(character["Health"]))

combat("wolf", wolf_health, wolf_attack, character, inventory)

print("\nCurrent Status:")
print(f"Health: {character['Health']}/{character['Max_Health']}")
print(f"Potions: {inventory['Health Potion']}")

campsite_menu(character, inventory)


print("\n" + "=" * 50)
print("You venture forward, leaving your campsite behind confident in your decisions.")
print("The trees grow dark, or is that just the light? It seems to be fading fast..")
print(
    "You trip over a gnarled root, revealing a great and almost unnaturally large tree blocking the path forward."
)
print(
    "By the time you register what it is, you realize it's much too late to do anything about it."
)
print(
    "Low in timbre but high in pitch you hear a god awful hideous screaching noise that sends vibrations through your whole body."
)
print("\n" + "=" * 50)

boss_fight(character, inventory)


# Commenting Save file out so it doesn't resave every time its run
# with open("save.json", "w") as file:
#     json.dump(character, file)

# print("Character saved!")
