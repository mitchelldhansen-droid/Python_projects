# import json
import random

from combat import (
    bandit_leader_combat,
    boss_fight,
    combat,
    owlbear_ambush,
    pixie_encounter,
    wolf_ambush,
)
from enemies import Enemy
from player import create_character
from save_game import load_game, offer_save
from utils import game_over


def game_start():
    print("Welcome to the game!")
    print("What would you like to do?")
    print("1. Start a new game")
    print("2. Load a saved game")
    choice = input("Enter your choice: ")
    if choice == "1":
        return None, "GAME_START"
    elif choice == "2":
        try:
            character, current_state = load_game()
            return character, current_state
        except FileNotFoundError:
            print("No save file found! Starting a new game...")
            current_state = "GAME_START"
            character = None
            return character, current_state
    else:
        print("Invalid choice. Please try again.")
        return game_start()


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
    character.restore_spell_slots()
    print("Your spell slots are fully restored.")

    character.inventory.add_item("Health Potion", 1)
    print("Searching the camp, you find a health potion left behind.")

    print("\nCurrent Status:")
    print(f"Health: {character.health}/{character.max_health}")
    print(f"Potions: {character.inventory.get_item_count('Health Potion')}")
    print(f"Spell Slots: {character.current_spell_slots}/{character.max_spell_slots}")
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


# ------------------------------------------------------------------------------------------------------------------
# Glade_path
def glade_path(character):
    print(
        "As you walk through the glade, the air grows thick with the scent of blooming flowers."
    )
    print(
        "The scent is pleasant, a semi-sweet relaxing aroma, and you take a deep breath."
    )
    print("You feel a sense of peace wash over you.")
    print(
        "As you walk into the glade, you're surrounded by nothing but a field of red flowers."
    )
    print("What were you doing? Why did you come here? You can't remember.")
    print(
        "You realize the flowers must be doing something to you, and panic begins to set in."
    )
    print("What do you do?")

    while True:
        print(
            "1. Rush through, trying to get to the edge of the flowers as quickly as possible."
        )
        print(
            "2. Move carefully, trying to avoid the flowers and slowing your breathing."
        )
        print("3. Look for another way out of the poppy field.")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("You take off, running as fast as your equipment will allow.")
            print("Your breaths are shallow and rapid. Poppy pollen fills your lungs")
            print(
                "This glade stretches for what seems like miles, you'll never make it in time."
            )
            print("You collapse, strained by the pollen you've breathed in.")
            damage = 25
            result = character.take_damage(damage)
            print(f"You lose {damage} health.")
            if result == "died":
                return "died"
            print("You collapse to your hands and knees.")
            print("You no longer feel the heat of the sun.")
            print("Dazed, you look up unsure of what looms above you.")
            guardian = Enemy("poppy_guardian")
            result = combat(guardian, character, depth=1)
            if result == "died":
                return "died"
            break
        elif choice == "2":
            print("You slow your pace, taking slow breaths.")
            print(
                "You cover your nose and mouth, trying to avoid the denser patches of flowers."
            )
            if character.health >= 50 or character.attack_power >= 15:
                print(
                    "Your strength of body allows you to push through the effects of the pollen."
                )
                print("You emerge from the glade, weakened, but alive.")
                damage = 15
                result = character.take_damage(damage)
                print(f"You lose {damage} health.")
                if result == "died":
                    return "died"
                break
            else:
                print("You're too weak to push through the effects of the pollen.")
                print("You collapse, the pollen overcoming you.")
                damage = 20
                result = character.take_damage(damage)
                print(f"You lose {damage} health.")
                if result == "died":
                    return "died"
                print("Something stirs in the flowers!")
                guardian = Enemy("poppy_guardian")
                result = combat(guardian, character, depth=1)
                if result == "died":
                    return "died"
                break
        elif choice == "3":
            print("\nYou scan the edges and spot a narrow unmarked trail!")
            print("It's longer, but avoids most of the poppies.")
            print("You still breathe in some pollen along the way...")
            result = character.take_damage(10)
            if result == "died":
                return "died"
            break
        else:
            print("Invalid choice.")
            continue
    print("\n" + "=" * 50)
    print("You've made it through the poppy field!")
    print("The experience has hardened you.")
    character.level_up()
    print("=" * 50)

    return "survived"


# Forest_path
def forest_path(character):
    print("\n" + "=" * 50)
    print(
        "You reenter the forest, having vanquished the Abomination earlier, you hope this time will be different."
    )
    print("As you walk deeper into the forest, you revisit the Abomination's hollow.")
    print("As you get closer, you notice a torch burning in someone's hand.")
    print("You see a fellow adventurer!")
    print(
        "'I know you're there, step into the light and join me.' the Adventurer says to you."
    )
    print("What do you do?")

    while True:
        print(
            "1. Explain you defeated the Abomination and see if the Adventurer will join you. (Power Check)."
        )
        print(
            "2. Offer gold to the Adventurer and see if they will join you. (10 gold)"
        )
        print(
            "3. Ignore the Adventurer, and try to sneak past them on your way to bypass the glade."
        )
        choice = input("Enter your choice: ")

        if choice == "1":
            # Stat check - based on attack power (looking capable)
            print(
                "\n'I could use someone with your skills,' you say. The strength of many beats the strength of one."
            )
            if character.attack_power >= 15:
                print("The adventurer looks you over and nods approvingly.")
                print("'You look like you can handle yourself. I'll join you.'")
                character.has_companion = True
                print("\nA companion has joined you!")
            else:
                print("The adventurer shakes their head.")
                print("'You don't look strong enough to be worth following.'")
                print("\nYou can still offer gold, or continue alone.")
                continue  # Let them try another option
        elif choice == "2":
            if character.inventory.get_item_count("Gold") >= 10:
                print("\nYou offer 10 gold pieces.")
                print("The adventurer's eyes light up.")
                print("'Gold speaks louder than words. I'm in.'")
                character.inventory.remove_item("Gold", 10)
                character.has_companion = True
                print("\nA companion has joined you!")
            else:
                print(
                    f"\nYou only have {character.inventory.get_item_count('Gold')} gold."
                )
                print("The adventurer scoffs. 'Come back when you have real coin.'")
                continue  # Let them try another option

        elif choice == "3":
            print(
                "\nYou dare not answer in case it's another trap, and continue on your way."
            )
            print(
                "You do not recruit the Adventurer, the next battle will be difficult without help."
            )
        else:
            print("Invalid choice.")
            continue

        print("\n" + "=" * 50)
        print("You continue down the forest path...")
        print("=" * 50)

        return "survived"


# ------------------------------------------------------------------------------------------------------------------


def path_choice(character):
    print("\n" + "=" * 50)
    print("Having dealt with the pixie, you must now choose a path")
    print("Which path do you choose?")
    print("1. Continue into the idyllic glade, risking the unknown for power untold")
    print(
        "2. Take the longer path back through the forest, avoiding the glade entirely"
    )
    print("Both paths offer something, both paths will challenge you.")
    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            print("You venture forth into the idyllic glade.")
            character.path_taken = "glade"
            return "glade"
        elif choice == "2":
            print(
                "You double back, returning to the devil you know for the devil you don't."
            )
            character.path_taken = "forest"
            return "forest"
        else:
            print("Invalid choice.")
            continue


if __name__ == "__main__":
    character, current_state = game_start()
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
                offer_save(character, "CAMPSITE_MENU")
                current_state = "BOSS_INTRO"
        elif current_state == "BOSS_INTRO":
            boss_intro()
            current_state = "BOSS_FIGHT"
        elif current_state == "BOSS_FIGHT":
            result = boss_fight(character)
            if result == "died":
                current_state = "GAME_ENDING"
            else:
                offer_save(character, "PIXIE_ENCOUNTER")
                current_state = "PIXIE_ENCOUNTER"
        elif current_state == "PIXIE_ENCOUNTER":
            result = pixie_encounter(character)
            if result == "died":
                current_state = "GAME_ENDING"
            else:
                current_state = "PATH_CHOICE"
        elif current_state == "PATH_CHOICE":
            result = path_choice(character)
            if result == "glade":
                current_state = "GLADE_PATH"
            else:
                current_state = "FOREST_PATH"
        elif current_state == "GLADE_PATH":
            result = glade_path(character)
            if result == "died":
                current_state = "GAME_ENDING"
            else:
                offer_save(character, "BANDIT_COMBAT")
                current_state = "BANDIT_COMBAT"
        elif current_state == "FOREST_PATH":
            result = forest_path(character)
            current_state = "BANDIT_COMBAT"
        elif current_state == "BANDIT_COMBAT":
            result = bandit_leader_combat(character)
            if result == "died":
                current_state = "GAME_ENDING"
            else:
                current_state = "VICTORY"
        elif current_state == "VICTORY":
            print("\n" + "=" * 50)
            print("Congratulations! You've completed the adventure!")
            if character:
                if character.path_taken == "glade":
                    print(
                        "\nBattered but powerful, you emerge from the wilderness alone."
                    )
                    print("The trials have made you stronger than you ever imagined.")
                elif character.path_taken == "forest" and character.has_companion:
                    print("\nYou and your ally share a moment of triumph.")
                    print("'Until next time, friend,' they say, clasping your hand.")
                elif character.path_taken == "forest":
                    print("\nYou made it through, though you walk alone.")
                print(f"\nThanks for playing, {character.name}!")
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
