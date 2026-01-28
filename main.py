# import json
import random

from combat import boss_fight, owlbear_ambush, pixie_encounter, wolf_ambush
from player import create_character
from utils import game_over

current_state = "GAME_START"


def rest(character, is_dangerous=False):
    print("\nYou decide to take advantage of the nearly setup camp.")
    print("The fire pit is cold but there's dry wood stacked nearby.")

    if is_dangerous:
        roll = random.random()
        if roll < 0.5:
            # Owlbear ambush while resting!
            result = owlbear_ambush(character)
            if result == "died":
                return "died"
            # After Owlbear, continue with the rest
            print("\nAfter the brutal fight, you finally get your rest...")
            return True
    if character.health < character.max_health:
        character.health = character.max_health
        print("You rest by the rekindled fire. Health fully restored!")
    else:
        print("You're already at full health, but the rest is welcome.")

    character.inventory.add_item("Health Potion", 1)
    print("Searching the camp, you find a health potion left behind.")

    print("\nCurrent Status:")
    print(f"Health: {character.health}/{character.max_health}")
    print(f"Potions: {character.inventory.get_item_count('Health Potion')}")

    return False


# ----------------------------------------------------------------------------------


def search(character, is_dangerous=False, depth=0):
    print("You decide to search around for any useful supplies")
    roll = random.random()
    if is_dangerous:
        # 50% Owlbear chance on dangerous search
        if roll < 0.5:
            result = owlbear_ambush(character)
            if result == "died":
                return "died"
            return True  # Owlbear happened
        else:
            # 50% split between potion and knife
            if roll < 0.75:  # 0.5 to 0.75 = 25% of total = 50% of remaining
                print(
                    "You find another health potion! They must have left in a hurry..."
                )
                character.inventory.add_item("Health Potion", 1)
            else:
                print("You find a small knife, it might come in handy.")
                character.inventory.add_item("Knife", 1)
            return False  # No Owlbear
    else:
        if roll < 0.5:
            print("You find another health potion! They must have left in a hurry...")
            character.inventory.add_item("Health Potion", 1)
            return False
        elif roll < 0.9:
            print("You find a small knife, it might come in handy.")
            character.inventory.add_item("Knife", 1)
            return False
        else:
            result = owlbear_ambush(character)
            if result == "died":
                return "died"
            return True  # Owlbear happened


# ----------------------------------------------------------------------------------


def campsite_menu(character):
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
            result = rest(character, is_dangerous=has_searched)
            if result == "died":
                return "died"
            has_rested = True
            if result is True:  # Owlbear happened but survived
                print("\nAfter that brutal fight, you must rest before continuing..")
                rest(character)
        elif choice == "2" and not has_searched:
            result = search(character, is_dangerous=has_rested)
            if result == "died":
                return "died"
            has_searched = True
            if result is True:  # Owlbear happened but survived
                print("\n After that brutal fight, you must rest before continuing..")
                rest(character)
                break
        elif choice == "3":
            break
        else:
            print("Invalid choice, select again.")
            continue
        if has_rested and has_searched:
            print("\n You've done what you can here, it's time to move on.")
            break
    return "survived"


# ----------------------------------------------------------------------------------


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


character = None
while True:
    if current_state == "GAME_START":
        character = create_character()
        character.display()
        current_state = "WOLF_COMBAT"
    elif current_state == "WOLF_COMBAT":
        result = wolf_ambush(character)
        if result == "died":
            current_state = "GAME_ENDING"
        else:
            current_state = "CAMPSITE_MENU"
    elif current_state == "CAMPSITE_MENU":
        result = campsite_menu(character)
        if result == "died":
            current_state = "GAME_ENDING"
        else:
            current_state = "BOSS_INTRO"
    elif current_state == "BOSS_INTRO":
        boss_intro()
        current_state = "BOSS_FIGHT"
    elif current_state == "BOSS_FIGHT":
        result = boss_fight(character)
        if result == "died":
            current_state = "GAME_ENDING"
        else:
            current_state = "PIXIE_ENCOUNTER"
    elif current_state == "PIXIE_ENCOUNTER":
        result = pixie_encounter(character)
        if result == "died":
            current_state = "GAME_ENDING"
        else:
            current_state = "VICTORY"
    elif current_state == "VICTORY":
        print("\n" + "=" * 50)
        print("Congratulations! You've completed the adventure!")
        if character:
            print(f"Thanks for playing, {character.name}!")
        print("=" * 50)
        break
    elif current_state == "GAME_ENDING":
        result = game_over(character)
        if result == "restart":
            current_state = "GAME_START"
        elif result == "quit":
            break


# Commenting Save file out so it doesn't resave every time its run
# with open("save.json", "w") as file:
#     json.dump(character, file)

# print("Character saved!")
