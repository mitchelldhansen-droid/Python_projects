import random

from enemies import Enemy


def combat(enemy, character, inventory, depth=0):
    print(f"a {enemy.name} appears! Health: {enemy.health}")
    while enemy.health > 0 and character.health > 0:
        skip_enemy_turn = False
        print(f"Your Health: {character.health} | Enemy Health: {enemy.health}")
        print(f"Potions Remaining: {inventory.get_item_count('Health Potion')}")
        print("What do you do??")
        print("1. Attack")
        print("2. Defend")
        print("3. Drink Potion")

        action = input("Choose 1., 2., or 3.")

        if action == "1":
            print(f"You attack the {enemy.name}!")
            enemy.take_damage(character.attack_power)
            print(f"{enemy.name} Health is now: {enemy.health}")
        elif action == "2":
            character.defend(enemy.attack_power)
            print(f"Health is now: {character.health}")
            skip_enemy_turn = True
        elif action == "3":
            result = character.use_potion()
            if result == "no_potion":
                continue
        else:
            print("Invalid action")
            continue
        if enemy.health <= 0:
            print(f"You defeated the {enemy.name}!")
            roll = random.random()
            if roll < 0.6:
                inventory.add_item("Health Potion")
                print(f"The {enemy.name} dropped a health potion! Added to inventory.")
            elif roll < 0.9:
                if depth < 1:
                    print("A skeleton clambors to life and attacks!")
                    skeleton = Enemy("skeleton")
                    result = combat(skeleton, character, inventory, depth + 1)
                    if result == "died":
                        return "died"
            else:
                print(f"The {enemy.name} had nothing useful..")
        elif character.health <= 0:
            print(f"You were defeated by the {enemy.name}!")
            return "died"
        elif not skip_enemy_turn:
            enemy.attack(character)
            print(f"Health is now: {character.health}")
    return "survived"


# ---------------------------------------------------------------------------------


def wolf_ambush(character, inventory):
    print(" ")
    print(
        "You hear a growling, and leaves rustle as something lifts off from the forest floor and the shape of a wolf lunges towards you! You take 10 damage"
    )
    character.health = character.health - 10
    print("Health is now: " + str(character.health))
    if character.health > 0:
        wolf = Enemy("wolf")
        result = combat(wolf, character, inventory)
        if result == "died":
            return "died"
    elif character.health <= 0:
        return "died"
    print("\nCurrent Status:")
    print(f"Health: {character.health}/{character.max_health}")
    print(f"Potions: {inventory.get_item_count('Health Potion')}")
    return "survived"


# ----------------------------------------------------------------------------------


def owlbear_ambush(character, inventory):
    print("Out of the darkness a huge shadow looms over you and attacks!")
    character.health = character.health - 15
    print("Health is now: " + str(character.health))
    owlbear = Enemy("owlbear")
    if character.health <= 0:
        return "died"
    else:
        result = combat(owlbear, character, inventory, depth=1)
        if result == "died":
            return "died"
        elif result == "survived":
            return "survived"


# ----------------------------------------------------------------------------------


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
    boss = Enemy("abomination")
    print(
        "You barely see it coming. A huge tentacle of absorbed flesh rends through the air cutting towards you."
    )
    character.health -= 20
    print(f"Your Health: {character.health}/{character.max_health}")
    if character.health <= 0:
        return "died"
    result = combat(boss, character, inventory, depth=0)
    if result == "died":
        return "died"
    else:
        print("\n" + "=" * 50)
        print("You emerge victorious, the Abomination's power absorbed into you.")
        print("You feel stronger, more resilient than ever before.")
        character.attack_power += 5
        character.magic += 5
        character.max_health += 15
        character.health = character.max_health
        print("+5 TO ALL STATS | +15 MAX HEALTH")
        print(
            f"Attack: {character.attack_power} | Magic: {character.magic} | Max Health: {character.max_health}"
        )
        print("Level Up!")
        print("VICTORY!")
        print("\n" + "=" * 50)
        return "survived"


# ----------------------------------------------------------------------
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
    if inventory.has_item("Knife"):
        # show trade or attack options
        print("You have a knife!")
        print("1. Trade")
        print("2. Attack")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("You trade your knife for a health potion.")
            inventory.remove_item("Knife")
            inventory.add_item("Health Potion")
            print(
                "The pixie is satisfied with your trade and smiles, and you notice she has tiny little daggers as teeth."
            )
            print("She inserts the dagger into her mouth, waves, and flies away.")
            print(
                "You have the feeling nothing here is going to make sense, and that you just avoided a difficult encounter."
            )
        elif choice == "2":
            print("You attack the pixie with your knife.")
            pixie = Enemy("pixie")
            original_health = pixie.health
            pixie.take_damage(character.attack_power)
            print(f"Health is now: {character.health}")
            result = combat(pixie, character, inventory, depth=0)
            if result == "died":
                return "died"
            print("The pixie reforms somehow!")
            pixie2 = Enemy("pixie")
            pixie2.health = original_health // 2
            result = combat(pixie2, character, inventory, depth=1)
            if result == "died":
                return "died"
            print(
                "The pixie finally dissolves in a burst of light! You are victorious!"
            )
            inventory.add_item("Gold", 10)
            inventory.add_item("Health Potion", 2)
        else:
            print("Invalid choice.")
    elif not inventory.has_item("Knife"):
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
            pixie = Enemy("pixie")
            original_health = pixie.health
            result = combat(pixie, character, inventory, depth=0)
            if result == "died":
                return "died"
            print("The pixie reforms somehow!")
            pixie2 = Enemy("pixie")
            pixie2.health = original_health // 2
            result = combat(pixie2, character, inventory, depth=1)
            if result == "died":
                return "died"
            print(
                "The pixie finally dissolves in a burst of light! You are victorious!"
            )
            inventory.add_item("Gold", 10)
            inventory.add_item("Health Potion", 2)
        elif choice == "2":
            print("You attack the pixie.")
            pixie = Enemy("pixie")
            original_health = pixie.health
            pixie.take_damage(character.attack_power)
            print(f"Health is now: {character.health}")
            result = combat(pixie, character, inventory, depth=0)
            if result == "died":
                return "died"
            print("The pixie reforms somehow!")
            pixie2 = Enemy("pixie")
            pixie2.health = original_health // 2
            result = combat(pixie2, character, inventory, depth=1)
            if result == "died":
                return "died"
            print(
                "The pixie finally dissolves in a burst of light! You are victorious!"
            )
            inventory.add_item("Gold", 10)
            inventory.add_item("Health Potion", 2)
        else:
            print("Invalid choice.")
    return "survived"
