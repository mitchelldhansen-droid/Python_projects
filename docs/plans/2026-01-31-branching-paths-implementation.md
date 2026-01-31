# Branching Paths Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add two branching narrative paths after the pixie encounter that converge at a final combat with path-specific bonuses.

**Architecture:** Extend the state machine with `PATH_CHOICE`, `GLADE_PATH`, `FOREST_PATH`, and `FINAL_COMBAT` states. Add `has_companion` and `path_taken` attributes to Character. Create new enemy types for glade combat and final boss.

**Tech Stack:** Python, existing class structure (Character, Enemy, Inventory)

---

## Task 1: Add New Enemy Types to Data

**Files:**
- Modify: `data/enemy_stats.py`

**Step 1: Add poppy_guardian and bandit to ENEMY_STATS**

Open `data/enemy_stats.py` and add two new enemies:

```python
ENEMY_STATS = {
    "wolf": {"health": (30, 50), "attack": (5, 10)},
    "owlbear": {"health": (40, 60), "attack": (8, 15)},
    "skeleton": {"health": (20, 35), "attack": (4, 8)},
    "abomination": {"health": (70, 85), "attack": (10, 12)},
    "pixie": {"health": (30, 35), "attack": (8, 10)},
    "poppy_guardian": {"health": (45, 55), "attack": (8, 12)},
    "bandit": {"health": (50, 65), "attack": (10, 14)},
}
```

**Step 2: Test manually**

Run Python and verify the new enemies work:
```bash
python -c "from enemies import Enemy; e = Enemy('poppy_guardian'); print(e.name, e.health, e.attack_power)"
```

Expected: `poppy_guardian` followed by numbers in the defined ranges.

**Step 3: Commit**

```bash
git add data/enemy_stats.py
git commit -m "Add poppy_guardian and bandit enemy types"
```

---

## Task 2: Add Character Attributes for Branching

**Files:**
- Modify: `player.py` (Character class `__init__` method)

**Step 1: Add has_companion and path_taken attributes**

In `player.py`, add two new attributes to the `Character.__init__` method after `self.inventory = Inventory()`:

```python
self.has_companion = False
self.path_taken = None  # Will be "glade" or "forest"
```

**Step 2: Test manually**

```bash
python -c "from player import Character; c = Character('Test', 'Warrior'); print(c.has_companion, c.path_taken)"
```

Expected: `False None`

**Step 3: Commit**

```bash
git add player.py
git commit -m "Add has_companion and path_taken attributes to Character"
```

---

## Task 3: Add level_up Method to Character

**Files:**
- Modify: `player.py` (Character class)

**Step 1: Add level_up method**

Add this method to the Character class (after `use_potion`):

```python
def level_up(self, health_bonus=10, attack_bonus=3):
    self.max_health += health_bonus
    self.health = self.max_health
    self.attack_power += attack_bonus
    print(f"\n{self.name} leveled up!")
    print(f"+{health_bonus} Max Health | +{attack_bonus} Attack")
    print(f"Health fully restored to {self.max_health}!")
```

**Step 2: Test manually**

```bash
python -c "from player import Character; c = Character('Test', 'Warrior'); print(c.max_health, c.attack_power); c.level_up(); print(c.max_health, c.attack_power)"
```

Expected: Initial stats, then level up message, then stats increased by 10 health and 3 attack.

**Step 3: Commit**

```bash
git add player.py
git commit -m "Add level_up method to Character class"
```

---

## Task 4: Create Path Choice Function

**Files:**
- Modify: `combat.py` (add new function at bottom)

**Step 1: Add path_choice function**

Add this function at the bottom of `combat.py`:

```python
def path_choice(character):
    print("\n" + "=" * 50)
    print("The pixie encounter behind you, you see the path ahead splits.")
    print("To the left, a beautiful clearing bathed in sunlight beckons.")
    print("To the right, a dense forest trail winds back the long way.")
    print("=" * 50)

    while True:
        print("\nWhich path do you take?")
        print("1. Continue to the clearing ahead")
        print("2. Turn back and take the forest trail")
        choice = input("Enter your choice: ")

        if choice == "1":
            character.path_taken = "glade"
            return "glade"
        elif choice == "2":
            character.path_taken = "forest"
            return "forest"
        else:
            print("Invalid choice.")
```

**Step 2: Test manually**

```bash
python -c "from player import Character; from combat import path_choice; c = Character('Test', 'Warrior'); result = path_choice(c); print(result, c.path_taken)"
```

Enter "1" when prompted.
Expected: `glade glade`

**Step 3: Commit**

```bash
git add combat.py
git commit -m "Add path_choice function for branching narrative"
```

---

## Task 5: Create Glade Path Function

**Files:**
- Modify: `combat.py` (add new function)

**Step 1: Add glade_path function**

Add this function to `combat.py` after `path_choice`:

```python
def glade_path(character):
    print("\n" + "=" * 50)
    print("You step into the clearing. Beautiful red poppies sway gently.")
    print("The air is thick and sweet. Almost... too sweet.")
    print("You feel drowsy. Something is wrong.")
    print("=" * 50)

    # Puzzle choice
    while True:
        print("\nThe poppies seem to stretch endlessly. How do you proceed?")
        print("1. Rush through as fast as possible")
        print("2. Move carefully, covering your nose")
        print("3. Look for another way around")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Rush - takes more damage, guaranteed combat
            print("\nYou sprint forward but the field is larger than it seemed!")
            print("The pollen overwhelms you and you collapse...")
            damage = 25
            result = character.take_damage(damage)
            if result == "died":
                return "died"
            print("\nYou wake to find something looming over you!")
            guardian = Enemy("poppy_guardian")
            result = combat(guardian, character, depth=1)
            if result == "died":
                return "died"
            break

        elif choice == "2":
            # Careful - stat check based on health
            print("\nYou cover your face and move slowly through the field...")
            if character.health >= 50:
                print("Your strength lets you push through the drowsiness!")
                print("You emerge on the other side, weakened but alive.")
                result = character.take_damage(15)
                if result == "died":
                    return "died"
            else:
                print("You're too weakened. The pollen overcomes you...")
                result = character.take_damage(20)
                if result == "died":
                    return "died"
                print("\nSomething stirs in the flowers!")
                guardian = Enemy("poppy_guardian")
                result = combat(guardian, character, depth=1)
                if result == "died":
                    return "died"
            break

        elif choice == "3":
            # Look around - best outcome but still costs some health
            print("\nYou scan the edges and spot a narrow deer trail!")
            print("It's longer but avoids most of the poppies.")
            print("You still breathe in some pollen along the way...")
            result = character.take_damage(10)
            if result == "died":
                return "died"
            break
        else:
            print("Invalid choice.")

    # Reward
    print("\n" + "=" * 50)
    print("You've made it through the poppy field!")
    print("The experience has hardened you.")
    character.level_up()
    print("=" * 50)

    return "survived"
```

**Step 2: Update imports at top of combat.py**

The `Enemy` import should already be there. Verify it exists:
```python
from enemies import Enemy
```

**Step 3: Test manually**

```bash
python -c "from player import Character; from combat import glade_path; c = Character('Test', 'Warrior'); c.health = 100; result = glade_path(c); print(result)"
```

Enter "3" for the easiest path. Expected: Narrative text, 10 damage taken, level up message, `survived`.

**Step 4: Commit**

```bash
git add combat.py
git commit -m "Add glade_path function with puzzle and stat checks"
```

---

## Task 6: Create Forest Path Function

**Files:**
- Modify: `combat.py` (add new function)

**Step 1: Add forest_path function**

Add this function to `combat.py` after `glade_path`:

```python
def forest_path(character):
    print("\n" + "=" * 50)
    print("You take the winding forest trail.")
    print("The trees are dense but the path is clear.")
    print("After some time, you spot a small campfire ahead.")
    print("A weary-looking adventurer sits beside it, sharpening a blade.")
    print("=" * 50)

    while True:
        print("\nThe adventurer notices you approach. What do you do?")
        print("1. Ask them to join you")
        print("2. Offer gold for their help (10 gold)")
        print("3. Leave them be")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Stat check - based on attack power (looking capable)
            print("\n'I could use someone with your skills,' you say.")
            if character.attack_power >= 20:
                print("The adventurer looks you over and nods approvingly.")
                print("'You look like you can handle yourself. I'll join you.'")
                character.has_companion = True
                print("\nA companion has joined you!")
            else:
                print("The adventurer shakes their head.")
                print("'You don't look strong enough to be worth following.'")
                print("\nYou can still offer gold, or continue alone.")
                continue  # Let them try another option
            break

        elif choice == "2":
            if character.inventory.get_item_count("Gold") >= 10:
                print("\nYou offer 10 gold pieces.")
                print("The adventurer's eyes light up.")
                print("'Gold speaks louder than words. I'm in.'")
                character.inventory.remove_item("Gold", 10)
                character.has_companion = True
                print("\nA companion has joined you!")
            else:
                print(f"\nYou only have {character.inventory.get_item_count('Gold')} gold.")
                print("The adventurer scoffs. 'Come back when you have real coin.'")
                continue  # Let them try another option
            break

        elif choice == "3":
            print("\nYou nod politely and continue on your way.")
            print("The adventurer returns to sharpening their blade.")
            break
        else:
            print("Invalid choice.")

    print("\n" + "=" * 50)
    print("You continue down the forest path...")
    print("=" * 50)

    return "survived"
```

**Step 2: Test manually**

```bash
python -c "from player import Character; from combat import forest_path; c = Character('Test', 'Warrior'); c.attack_power = 25; result = forest_path(c); print(result, c.has_companion)"
```

Enter "1" when prompted. Expected: Success message, `survived True`.

**Step 3: Commit**

```bash
git add combat.py
git commit -m "Add forest_path function with adventurer recruitment"
```

---

## Task 7: Create Final Combat Function

**Files:**
- Modify: `combat.py` (add new function)

**Step 1: Add final_combat function**

Add this function to `combat.py` after `forest_path`:

```python
def final_combat(character):
    print("\n" + "=" * 50)
    print("As you near the edge of the wilderness, a figure blocks your path.")
    print("A scarred bandit emerges from the shadows, blade drawn.")
    print("'Your journey ends here, traveler. Hand over your valuables.'")
    print("=" * 50)

    if character.has_companion:
        print("\nYour companion steps forward beside you.")
        print("'Two against one. You sure about this?'")
        print("The bandit hesitates but raises their blade anyway.")

    bandit = Enemy("bandit")

    # Modified combat for companion bonus
    print(f"\nA {bandit.name} attacks! Health: {bandit.health}")

    while bandit.health > 0 and character.health > 0:
        skip_enemy_turn = False
        print(f"\nYour Health: {character.health} | Enemy Health: {bandit.health}")
        print(f"Potions: {character.inventory.get_item_count('Health Potion')}")
        if character.has_companion:
            print("(Companion doubles your attack damage!)")
        print("\nWhat do you do?")
        print("1. Attack")
        print("2. Defend")
        print("3. Drink Potion")

        action = input("Choose 1, 2, or 3: ")

        if action == "1":
            damage = character.attack_power
            if character.has_companion:
                damage = damage * 2
                print(f"You and your companion strike together!")
            else:
                print(f"You attack the {bandit.name}!")
            bandit.take_damage(damage)
            print(f"{bandit.name} Health is now: {bandit.health}")
        elif action == "2":
            character.defend(bandit.attack_power)
            skip_enemy_turn = True
        elif action == "3":
            result = character.use_potion()
            if result == "no_potion":
                continue
        else:
            print("Invalid action")
            continue

        if bandit.health <= 0:
            print(f"\nYou defeated the {bandit.name}!")
            break
        elif character.health <= 0:
            print(f"\nYou were defeated by the {bandit.name}!")
            return "died"
        elif not skip_enemy_turn:
            bandit.attack(character)

    return "survived"
```

**Step 2: Test manually**

```bash
python -c "from player import Character; from combat import final_combat; c = Character('Test', 'Warrior'); c.health = 100; c.attack_power = 30; c.has_companion = True; result = final_combat(c)"
```

Attack a few times. Expected: Doubled damage messages when attacking.

**Step 3: Commit**

```bash
git add combat.py
git commit -m "Add final_combat function with companion damage bonus"
```

---

## Task 8: Update Victory State for Endings

**Files:**
- Modify: `main.py` (VICTORY state)

**Step 1: Replace VICTORY block with path-aware endings**

Find the `elif current_state == "VICTORY":` block in `main.py` and replace it:

```python
    elif current_state == "VICTORY":
        print("\n" + "=" * 50)
        print("Congratulations! You've completed the adventure!")

        # Path-specific ending
        if character.path_taken == "glade":
            print("\nBattered but powerful, you emerge from the wilderness alone.")
            print("The trials have made you stronger than you ever imagined.")
        elif character.path_taken == "forest" and character.has_companion:
            print("\nYou and your new ally share a moment of triumph.")
            print("The journey forged a bond between you.")
            print("'Until next time, friend,' they say, clasping your hand.")
        elif character.path_taken == "forest":
            print("\nYou make it through, though you walk alone.")
            print("You wonder what might have been if you'd convinced that adventurer to join.")

        if character:
            print(f"\nThanks for playing, {character.name}!")
        print("=" * 50)
        break
```

**Step 2: Commit**

```bash
git add main.py
git commit -m "Add path-aware victory endings"
```

---

## Task 9: Update Imports in main.py

**Files:**
- Modify: `main.py` (import statement)

**Step 1: Add new function imports**

Update the imports at the top of `main.py`:

```python
from combat import (
    boss_fight,
    final_combat,
    forest_path,
    glade_path,
    owlbear_ambush,
    path_choice,
    pixie_encounter,
    wolf_ambush,
)
```

**Step 2: Commit**

```bash
git add main.py
git commit -m "Import new path functions in main.py"
```

---

## Task 10: Add New States to Game Loop

**Files:**
- Modify: `main.py` (game loop)

**Step 1: Update PIXIE_ENCOUNTER to go to PATH_CHOICE**

Find this block:
```python
    elif current_state == "PIXIE_ENCOUNTER":
        result = pixie_encounter(character)
        if result == "died":
            current_state = "GAME_ENDING"
        else:
            current_state = "VICTORY"
```

Replace `current_state = "VICTORY"` with:
```python
            current_state = "PATH_CHOICE"
```

**Step 2: Add PATH_CHOICE state**

Add after the PIXIE_ENCOUNTER block:

```python
    elif current_state == "PATH_CHOICE":
        result = path_choice(character)
        if result == "glade":
            current_state = "GLADE_PATH"
        else:
            current_state = "FOREST_PATH"
```

**Step 3: Add GLADE_PATH state**

Add after PATH_CHOICE:

```python
    elif current_state == "GLADE_PATH":
        result = glade_path(character)
        if result == "died":
            current_state = "GAME_ENDING"
        else:
            current_state = "FINAL_COMBAT"
```

**Step 4: Add FOREST_PATH state**

Add after GLADE_PATH:

```python
    elif current_state == "FOREST_PATH":
        result = forest_path(character)
        current_state = "FINAL_COMBAT"
```

**Step 5: Add FINAL_COMBAT state**

Add after FOREST_PATH:

```python
    elif current_state == "FINAL_COMBAT":
        result = final_combat(character)
        if result == "died":
            current_state = "GAME_ENDING"
        else:
            current_state = "VICTORY"
```

**Step 6: Commit**

```bash
git add main.py
git commit -m "Add branching path states to game loop"
```

---

## Task 11: Full Playthrough Test

**Step 1: Run the game and test both paths**

```bash
python main.py
```

**Test Path 1 (Glade):**
- Play through to pixie encounter
- Choose "Continue to the clearing"
- Try option 3 (deer trail) for easiest path
- Fight the bandit
- Verify glade ending text

**Test Path 2 (Forest with companion):**
- Restart game
- Play through to pixie encounter
- Choose "Forest trail"
- If you have 10 gold, offer gold to recruit
- Fight bandit (verify double damage)
- Verify companion ending text

**Test Path 3 (Forest alone):**
- Restart, low stats, no gold
- Choose forest, fail recruitment, leave alone
- Verify alone ending text

**Step 2: Commit final verification**

```bash
git add -A
git commit -m "Complete branching paths feature - tested all paths"
```

---

## Summary

**New files created:** None

**Files modified:**
- `data/enemy_stats.py` - Added 2 new enemy types
- `player.py` - Added `has_companion`, `path_taken`, and `level_up()` method
- `combat.py` - Added 4 new functions: `path_choice`, `glade_path`, `forest_path`, `final_combat`
- `main.py` - Updated imports, added 4 new states, updated victory endings

**Total commits:** 11 small commits

**Skills practiced:**
- Branching state machines
- Stat checks and conditional logic
- Storing/checking player choices across states
- Multiple paths converging
