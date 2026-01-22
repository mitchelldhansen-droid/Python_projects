# import json
import random

from combat import combat, pixie_encounter
from player import create_character, display_character
from utils import spawn_enemy

character, inventory = create_character()


display_character(character)


def owlbear_ambush(character, inventory):
    print("Out of the darkness a huge shadow looms over you and attacks!")
    character["Health"] = (character["Health"]) - 15
    print("Health is now: " + str(character["Health"]))
    owlbear_health, owlbear_attack = spawn_enemy("owlbear")
    if character["Health"] <= 0:
        print("You were defeated by the Owlbear!")
        print("GAME OVER")
        exit()
    else:
        combat("Owlbear", owlbear_health, owlbear_attack, character, inventory, depth=1)
    return True


def rest(character, inventory, is_dangerous=False):
    print("\nYou decide to take advantage of the nearly setup camp.")
    print("The fire pit is cold but there's dry wood stacked nearby.")

    if is_dangerous:
        roll = random.random()
        if roll < 0.5:
            # Owlbear ambush while resting!
            owlbear_ambush(character, inventory)
            # After Owlbear, continue with the rest
            print("\nAfter the brutal fight, you finally get your rest...")
            return True
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
            owlbear_ambush(character, inventory)
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
            owlbear_ambush(character, inventory)
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
    boss_health, boss_attack = spawn_enemy("abomination")
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
    else:
        print("You have been defeated!")
        print("GAME OVER")
        exit()


def wolf_ambush(character, inventory):
    print(" ")
    print(
        "You hear a growling, and leaves rustle as something lifts off from the forest floor and the shape of a wolf lunges towards you! You take 10 damage"
    )
    character["Health"] = character["Health"] - 10
    print("Health is now: " + str(character["Health"]))
    if character["Health"] > 0:
        wolf_health, wolf_attack = spawn_enemy("wolf")
        combat("wolf", wolf_health, wolf_attack, character, inventory)
    elif character["Health"] <= 0:
        print("You have been defeated!")
        print("GAME OVER")
        exit()
    print("\nCurrent Status:")
    print(f"Health: {character['Health']}/{character['Max_Health']}")
    print(f"Potions: {inventory['Health Potion']}")


def boss_intro():
    print("\n" + "=" * 50)
    print(
        "You venture forward, leaving your campsite behind confident in your decisions."
    )
    print(
        "The trees grow dark, or is that just the light? It seems to be fading fast.."
    )
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


wolf_ambush(character, inventory)

campsite_menu(character, inventory)

boss_intro()

boss_fight(character, inventory)

print("\n" + "=" * 50)

pixie_encounter(character, inventory)

# Commenting Save file out so it doesn't resave every time its run
# with open("save.json", "w") as file:
#     json.dump(character, file)

# print("Character saved!")
