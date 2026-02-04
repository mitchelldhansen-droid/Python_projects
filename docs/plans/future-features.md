# Future Feature Plans

Two features to implement that transfer directly to Godot/GDScript.

---

# Feature 1: Save/Load System

## Goal
Save game progress to a file, load it back later. Learn serialization - converting objects to data and back.

## Why This Matters for Godot
Godot uses the same pattern: convert game state to dictionaries, save to JSON or binary. You'll use this for Project Zelena to save dialogue progress, player choices, etc.

---

## The Challenge

Your `Character` object has:
- Simple values: `name`, `health`, `level` (easy to save)
- Nested object: `inventory` (needs special handling)
- Signal objects: `damaged`, `healed`, `died` (can't be saved - must recreate)

You can't just dump the object to a file. You need to:
1. Convert to a dictionary of simple values
2. Save that dictionary to JSON
3. Load the dictionary back
4. Recreate the object from that data

---

## Phase 1: Add `to_dict()` to Character

Add a method that extracts saveable data:

```python
def to_dict(self):
    return {
        "name": self.name,
        "player_class": self.player_class,
        "health": self.health,
        "max_health": self.max_health,
        "attack_power": self.attack_power,
        "magic": self.magic,
        "level": self.level,
        "has_companion": self.has_companion,
        "path_taken": self.path_taken,
        "current_spell_slots": self.current_spell_slots,
        "max_spell_slots": self.max_spell_slots,
        "inventory": self.inventory.items  # just the dict, not the object
    }
```

**Test:** Create character, call `to_dict()`, print result.

---

## Phase 2: Add `from_dict()` classmethod

A classmethod creates an instance from saved data:

```python
@classmethod
def from_dict(cls, data):
    # Create character with basic info
    character = cls(data["name"], data["player_class"])

    # Override calculated values with saved values
    character.health = data["health"]
    character.max_health = data["max_health"]
    character.attack_power = data["attack_power"]
    character.magic = data["magic"]
    character.level = data["level"]
    character.has_companion = data["has_companion"]
    character.path_taken = data["path_taken"]
    character.current_spell_slots = data["current_spell_slots"]
    character.max_spell_slots = data["max_spell_slots"]
    character.inventory.items = data["inventory"]

    return character
```

**Test:** Create character, modify stats, convert to dict, create new character from dict, verify values match.

---

## Phase 3: Create save/load functions

Create `save_game.py`:

```python
import json

def save_game(character, current_state, filename="savegame.json"):
    data = {
        "character": character.to_dict(),
        "current_state": current_state
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print("Game saved!")

def load_game(filename="savegame.json"):
    with open(filename, "r") as f:
        data = json.load(f)

    from player import Character
    character = Character.from_dict(data["character"])
    current_state = data["current_state"]

    print("Game loaded!")
    return character, current_state
```

**Test:** Save game, check file exists, load game, verify character state.

---

## Phase 4: Integrate into main.py

Add save/load options to appropriate places:

1. **Save prompt after campsite:** Ask "Save your progress? (y/n)"
2. **Load option at game start:** "1. New Game  2. Load Game"
3. **Handle missing save file:** Try/except for FileNotFoundError

---

## Files Summary

| File | Action |
|------|--------|
| `player.py` | ADD `to_dict()` and `from_dict()` methods |
| `save_game.py` | CREATE save/load functions |
| `main.py` | MODIFY to add save/load prompts |

---

## Git Workflow

```bash
git checkout -b feature/save-load
# Commit after each phase
git checkout main && git merge feature/save-load
```

---

## Godot Equivalent

**Python (what you'll build):**
```python
data = character.to_dict()
json.dump(data, file)
```

**GDScript (what you'll write in Godot):**
```gdscript
var data = character.to_dict()
var file = FileAccess.open("save.json", FileAccess.WRITE)
file.store_string(JSON.stringify(data))
```

Nearly identical pattern.

---
---

# Feature 2: Class-Based State Machine

## Goal
Upgrade your string-based state machine to use classes. Each state becomes its own class with `enter()`, `update()`, and `exit()` methods.

## Why This Matters for Godot
Godot uses this exact pattern for game states, animation states, AI behavior. It's cleaner and more scalable than string comparisons.

---

## Current State Machine

Your current approach uses strings:

```python
current_state = "GAME_START"

while True:
    if current_state == "GAME_START":
        # do stuff
        current_state = "WOLF_COMBAT"
    elif current_state == "WOLF_COMBAT":
        # do stuff
        current_state = "CAMPSITE_MENU"
    # ... etc
```

**Problems:**
- Adding new states means adding more elif branches
- State-specific logic is mixed together in one big file
- Hard to see what each state does at a glance

---

## Class-Based Approach

Each state becomes a class:

```python
class GameStartState:
    def enter(self, game):
        """Called when entering this state"""
        pass

    def update(self, game):
        """Called each frame/tick - returns next state or None"""
        character = create_character()
        character.display()
        game.character = character
        return WolfCombatState()  # return next state

    def exit(self, game):
        """Called when leaving this state"""
        pass
```

The main loop becomes simple:

```python
current_state = GameStartState()

while current_state:
    current_state.enter(game)
    next_state = current_state.update(game)
    current_state.exit(game)
    current_state = next_state
```

---

## Phase 1: Create State base class

Create `states.py`:

```python
class State:
    """Base class for all game states"""

    def enter(self, game):
        """Called when entering this state"""
        pass

    def update(self, game):
        """Main logic - returns next State or None to quit"""
        raise NotImplementedError

    def exit(self, game):
        """Called when leaving this state"""
        pass
```

---

## Phase 2: Create Game class to hold shared data

```python
class Game:
    """Holds all game data passed between states"""

    def __init__(self):
        self.character = None
        self.running = True
```

---

## Phase 3: Convert states one at a time

Start with simple states:

```python
class GameStartState(State):
    def update(self, game):
        game.character = create_character()
        game.character.display()
        return WolfCombatState()

class WolfCombatState(State):
    def update(self, game):
        result = wolf_ambush(game.character)
        if result == "died":
            return GameEndingState()
        return CampsiteMenuState()

class VictoryState(State):
    def update(self, game):
        print("Congratulations! You've completed the adventure!")
        # ... victory text ...
        return None  # None ends the game
```

---

## Phase 4: Update main loop

```python
if __name__ == "__main__":
    game = Game()
    current_state = GameStartState()

    while current_state:
        current_state.enter(game)
        next_state = current_state.update(game)
        current_state.exit(game)
        current_state = next_state
```

---

## Files Summary

| File | Action |
|------|--------|
| `states.py` | CREATE - State base class + all state classes |
| `game.py` | CREATE - Game class to hold shared data |
| `main.py` | MODIFY - simplify to use state machine |

---

## State List

Convert these states (in order):
1. `GameStartState`
2. `WolfCombatState`
3. `CampsiteMenuState`
4. `BossIntroState`
5. `BossFightState`
6. `PixieEncounterState`
7. `PathChoiceState`
8. `GladePathState`
9. `ForestPathState`
10. `BanditCombatState`
11. `VictoryState`
12. `GameEndingState`

---

## Git Workflow

```bash
git checkout -b feature/state-machine
# Convert 2-3 states per commit
git checkout main && git merge feature/state-machine
```

---

## Godot Equivalent

**Python (what you'll build):**
```python
class WolfCombatState(State):
    def update(self, game):
        result = wolf_ambush(game.character)
        if result == "died":
            return GameEndingState()
        return CampsiteMenuState()
```

**GDScript (what you'll write in Godot):**
```gdscript
class_name WolfCombatState extends State

func update(game: Game) -> State:
    var result = wolf_ambush(game.character)
    if result == "died":
        return GameEndingState.new()
    return CampsiteMenuState.new()
```

Same pattern, slightly different syntax.

---

## Recommendation

**Do Save/Load first** - it's more immediately useful and simpler.

**Do State Machine second** - it's a bigger refactor but worth it for the cleaner architecture.
