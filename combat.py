import random

from enemies import Enemy
from spells import cast_spell, display_spell_menu


def combat(enemy, character, depth=0):
    print(f"a {enemy.name} appears! Health: {enemy.health}")

    # Define listener functions
    def on_char_damaged(c, amt):
        print(f"{c.name} has taken {amt} damage. Health: {c.health}")

    def on_char_died(c):
        print(f"{c.name} has been defeated!")

    def on_enemy_damaged(e, amt):
        print(f"{e.name} has taken {amt} damage. Health: {e.health}")

    def on_enemy_died(e):
        print(f"{e.name} has been defeated!")

    # Connect them
    character.damaged.connect(on_char_damaged)
    character.died.connect(on_char_died)
    enemy.damaged.connect(on_enemy_damaged)
    enemy.died.connect(on_enemy_died)

    while enemy.health > 0 and character.health > 0:
        skip_enemy_turn = False
        print(f"Your Health: {character.health} | Enemy Health: {enemy.health}")
        print(
            f"Potions Remaining: {character.inventory.get_item_count('Health Potion')}"
        )
        print(
            f"Spells Remaining: {character.current_spell_slots}/{character.max_spell_slots}"
        )
        print("What do you do??")
        print("1. Attack")
        print("2. Defend")
        print("3. Drink Potion")
        print("4. Cast Spell")

        action = input("Choose 1., 2., 3., or 4.")

        if action == "1":
            print(f"You attack the {enemy.name}!")
            damage = character.attack_power
            if "attack_bonus" in character.active_buffs:
                bonus = character.active_buffs.pop("attack_bonus")
                damage += bonus
                print(f"Your spell adds {bonus} damage!")
            enemy.take_damage(damage)
            print(f"{enemy.name} Health is now: {enemy.health}")
        elif action == "2":
            character.defend(enemy.attack_power)
            print(f"Health is now: {character.health}")
            skip_enemy_turn = True
        elif action == "3":
            result = character.use_potion()
            if result == "no_potion":
                continue
        elif action == "4":
            spell_keys = display_spell_menu(character)
            spell_choice = input("Choose a spell (or 'back' to cancel): ")
            if spell_choice.lower() == "back":
                continue
            try:
                index = int(spell_choice) - 1
                if 0 <= index < len(spell_keys):
                    spell_key = spell_keys[index]
                    result = cast_spell(character, spell_key, target=enemy)
                    print(result["message"])
                    if not result["success"]:
                        continue
                else:
                    print("Invalid spell choice")
                    continue
            except (ValueError, IndexError):
                print("Invalid spell choice.")
                continue
        else:
            print("Invalid action")
            continue
        if enemy.health <= 0:
            print(f"You defeated the {enemy.name}!")
            roll = random.random()
            if roll < 0.6:
                character.inventory.add_item("Health Potion")
                print(f"The {enemy.name} dropped a health potion! Added to inventory.")
            elif roll < 0.9:
                if depth < 1:
                    print("A skeleton clambors to life and attacks!")
                    skeleton = Enemy("skeleton")
                    result = combat(skeleton, character, depth + 1)
                    if result == "died":
                        character.damaged.disconnect(on_char_damaged)
                        character.died.disconnect(on_char_died)
                        return "died"
            else:
                print(f"The {enemy.name} had nothing useful..")
        elif character.health <= 0:
            print(f"You were defeated by the {enemy.name}!")
            character.damaged.disconnect(on_char_damaged)
            character.died.disconnect(on_char_died)
            return "died"
        elif not skip_enemy_turn:
            if "dodge" in character.active_buffs:
                character.active_buffs.pop("dodge")
                print(f"You dodged the {enemy.name}'s attack!")
            elif "shield" in character.active_buffs:
                shield_value = character.active_buffs.pop("shield")
                blocked = min(shield_value, enemy.attack_power)
                remaining_damage = enemy.attack_power - blocked
                print(f"Your shield absorbs {blocked} damage!")
                if remaining_damage > 0:
                    character.take_damage(remaining_damage)
                print(f"Health is now: {character.health}")
            else:
                enemy.attack(character)
                print(f"Health is now: {character.health}")
            if character.health <= 0:
                print(f"You were defeated by the {enemy.name}!")
                character.damaged.disconnect(on_char_damaged)
                character.died.disconnect(on_char_died)
                return "died"

    character.damaged.disconnect(on_char_damaged)
    character.died.disconnect(on_char_died)
    return "survived"


# ---------------------------------------------------------------------------------


def wolf_ambush(character):
    print(" ")
    print(
        "You hear a growling, and leaves rustle as something lifts off from the forest floor and the shape of a wolf lunges towards you! You take 10 damage"
    )
    result = character.take_damage(10)
    if result == "died":
        return "died"
    wolf = Enemy("wolf")
    result = combat(wolf, character)
    if result == "died":
        return "died"
    print("\nCurrent Status:")
    print(f"Health: {character.health}/{character.max_health}")
    print(f"Potions: {character.inventory.get_item_count('Health Potion')}")
    return "survived"


# ----------------------------------------------------------------------------------


def owlbear_ambush(character):
    print("Out of the darkness a huge shadow looms over you and attacks!")
    result = character.take_damage(15)
    if result == "died":
        return "died"
    owlbear = Enemy("owlbear")
    result = combat(owlbear, character, depth=1)
    if result == "died":
        return "died"
    elif result == "survived":
        return "survived"


# ----------------------------------------------------------------------------------


def boss_fight(character):
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
    result = character.take_damage(20)
    if result == "died":
        return "died"
    result = combat(boss, character, depth=0)
    if result == "died":
        return "died"
    else:
        print("\n" + "=" * 50)
        print("You emerge victorious, the Abomination's power absorbed into you.")
        print("You feel stronger, more resilient than ever before.")
        character.level_up()
        print("VICTORY!")
        print("\n" + "=" * 50)
        return "survived"


# -------------------------------------------------------------------------------
def pixie_combat(character, first_strike=False):
    pixie = Enemy("pixie")
    original_health = pixie.health
    if first_strike:
        pixie.take_damage(character.attack_power)
        print(f"Health is now: {character.health}")
    result = combat(pixie, character, depth=0)
    if result == "died":
        return "died"
    print("The pixie reforms somehow!")
    pixie2 = Enemy("pixie")
    pixie2.health = original_health // 2
    result = combat(pixie2, character, depth=1)
    if result == "died":
        return "died"
    print("The pixie finally dissolves in a burst of light! You are victorious!")
    character.inventory.add_item("Gold", 10)
    character.inventory.add_item("Health Potion", 2)
    return "survived"


# ----------------------------------------------------------------------
def pixie_encounter(character):
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
    if character.inventory.has_item("Knife"):
        # show trade or attack options
        print("You have a knife!")
        print("1. Trade")
        print("2. Attack")
        while True:
            choice = input("Enter your choice: ")
            if choice == "1":
                print("You trade your knife for a health potion.")
                character.inventory.remove_item("Knife")
                character.inventory.add_item("Health Potion")
                print(
                    "The pixie is satisfied with your trade and smiles, and you notice she has tiny little daggers as teeth."
                )
                print("She inserts the dagger into her mouth, waves, and flies away.")
                print(
                    "You have the feeling nothing here is going to make sense, and that you just avoided a difficult encounter."
                )
                break
            elif choice == "2":
                print("You attack the pixie with your knife before she can react!")
                result = pixie_combat(character, first_strike=True)
                if result == "died":
                    return "died"
                break
            else:
                print("Invalid choice.")
    elif not character.inventory.has_item("Knife"):
        # show lie or attack options
        print("You don't have a knife.")
        print("1. Lie")
        print("2. Attack")
        while True:
            choice = input("Enter your choice: ")
            if choice == "1":
                print("You lie to the pixie.")
                print("The pixie is not convinced.")
                print("You dare deceive me?")
                print("She lunges at you with unnatural speed!")
                result = pixie_combat(character, first_strike=False)
                if result == "died":
                    return "died"
                break
            elif choice == "2":
                print("You attack the pixie outright!")
                result = pixie_combat(character, first_strike=True)
                if result == "died":
                    return "died"
                break
            else:
                print("Invalid choice.")
    return "survived"


def bandit_leader_combat(character):
    print("\n" + "=" * 50)
    if character.path_taken == "glade":
        print(
            "After narrowly escaping the poppy field, you notice a bandit group blocking your path at the edge of the wilderness."
        )
        print(
            "'You must be very sleepy after all them poppies, why don't you just turn around and march home. This here's Black Flag territory.' the bandit leader says."
        )
    elif character.path_taken == "forest":
        print("You approach the edge of the wilderness cautiously.")
        print("You notice a bandit group blocking your path.")
        print(
            "'Come out, come out, wherever you are! I wanna have some FUN!' The bandit leader says."
        )
    print(
        "'If you wanna pass, you'll have to make it through me.' the bandit leader says."
    )
    print("You ready yourself for battle.")
    if character.has_companion:
        print("Your companion steps forward, ready to fight alongside you.")
        print(
            "'I used to run with the black flag gang, when I challenged the leader, I got sentenced to exile in the forest' your companion says."
        )
        print(
            "'Together, we might be able to challenge him to a duel and take him down.'"
        )
    bandit_leader = Enemy("bandit_leader")

    # Define listener functions
    def on_char_damaged(c, amt):
        print(f"{c.name} has taken {amt} damage. Health: {c.health}")

    def on_char_died(c):
        print(f"{c.name} has been defeated!")

    def on_enemy_damaged(e, amt):
        print(f"{e.name} has taken {amt} damage. Health: {e.health}")

    def on_enemy_died(e):
        print(f"{e.name} has been defeated!")

    # Connect them
    character.damaged.connect(on_char_damaged)
    character.died.connect(on_char_died)
    bandit_leader.damaged.connect(on_enemy_damaged)
    bandit_leader.died.connect(on_enemy_died)

    while bandit_leader.health > 0 and character.health > 0:
        skip_enemy_turn = False
        print(
            f"\nYour Health: {character.health} | Enemy Health: {bandit_leader.health}"
        )
        print(f"Potions: {character.inventory.get_item_count('Health Potion')}")
        print(
            f"Spell Slots: {character.current_spell_slots}/{character.max_spell_slots}"
        )
        if character.has_companion:
            print(
                "(Through coordinated strikes, Your Companion doubles your attack damage!)"
            )
        print("1.Attack")
        print("2.Defend")
        print("3.Drink Potion")
        print("4.Cast Spell")
        action = input("Choose 1, 2, 3, or 4:")
        if action == "1":
            damage = character.attack_power
            if "attack_bonus" in character.active_buffs:
                bonus = character.active_buffs.pop("attack_bonus")
                damage += bonus
                print(f"Your spell adds {bonus} damage!")
            if character.has_companion:
                damage = damage * 2
                print("You and your companion strike together!")
            else:
                print("You attack the bandit leader!")
            bandit_leader.take_damage(damage)
            print(f"Bandit Leader's Health: {bandit_leader.health}")
        elif action == "2":
            character.defend(bandit_leader.attack_power)
            print("You defend yourself!")
            skip_enemy_turn = True
        elif action == "3":
            result = character.use_potion()
            if result == "no_potion":
                continue
        elif action == "4":
            spell_keys = display_spell_menu(character)
            spell_choice = input("Choose a spell (or 'back' to cancel): ")
            if spell_choice.lower() == "back":
                continue
            try:
                index = int(spell_choice) - 1
                if 0 <= index < len(spell_keys):
                    spell_key = spell_keys[index]
                    result = cast_spell(character, spell_key, target=bandit_leader)
                    print(result["message"])
                    if not result["success"]:
                        continue
                else:
                    print("Invalid spell choice")
                    continue
            except (ValueError, IndexError):
                print("Invalid spell choice.")
                continue
        else:
            print("Invalid action!")
            continue
        if bandit_leader.health <= 0:
            print("You defeated the bandit leader!")
            print("\n" + "=" * 50)
            print(
                "You emerge victorious, none of the bandits dare question your strength after defeating their leader."
            )
            print("Your reputation grows, and you become a legend in the land.")
            character.level_up()
            print("VICTORY!")
            print("\n" + "=" * 50)
            # Any victory rewards/narrative here
        elif character.health <= 0:
            print("You were defeated by the bandit leader!")
            character.damaged.disconnect(on_char_damaged)
            character.died.disconnect(on_char_died)
            return "died"
        elif not skip_enemy_turn:
            if "dodge" in character.active_buffs:
                character.active_buffs.pop("dodge")
                print(f"You dodge the {bandit_leader.name}'s attack!")
            elif "shield" in character.active_buffs:
                shield_value = character.active_buffs.pop("shield")
                blocked = min(shield_value, bandit_leader.attack_power)
                remaining_damage = bandit_leader.attack_power - blocked
                print(f"Your shield absorbs {blocked} damage!")
                if remaining_damage > 0:
                    character.take_damage(remaining_damage)
                print(f"Health is now: {character.health}")
            else:
                bandit_leader.attack(character)
                print(f"Health is now: {character.health}")
            if character.health <= 0:
                print(f"You were defeated by the {bandit_leader.name}!")
                character.damaged.disconnect(on_char_damaged)
                character.died.disconnect(on_char_died)
                return "died"

    character.damaged.disconnect(on_char_damaged)
    character.died.disconnect(on_char_died)
    return "survived"
