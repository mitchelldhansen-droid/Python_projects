# Python Text RPG

A text-based RPG adventure built in Python as a learning project. Navigate a dark forest, fight monsters, make choices that shape your journey, and defeat the bandit leader to win.

## How to Play

```bash
python main.py
```

No external dependencies required — runs on Python 3 standard library only.

## Gameplay

You create a character by choosing a name and class, then progress through a series of encounters connected by a state machine. Choices you make affect your path, available resources, and story outcomes.

### Classes

| Class   | Health | Attack | Magic | Spell Slots |
|---------|--------|--------|-------|-------------|
| Warrior | 100    | 15     | 5     | 2           |
| Mage    | 60     | 5      | 20    | 5           |
| Rogue   | 75     | 12     | 8     | 3           |
| Paladin | 85     | 10     | 12    | 4           |

Each class has unique spells (damage, healing, buffs, shields, dodge) that consume spell slots.

### Adventure Flow

1. **Wolf Ambush** — A wolf attacks you on the road
2. **Campsite** — Rest to heal, search for supplies, or push onward (with risk of owlbear ambush)
3. **The Abomination** — A boss fight against a twisted creature in the dark forest
4. **Pixie Encounter** — Trade, lie, or fight — outcomes depend on your inventory
5. **Path Choice** — Two branching routes:
   - **Glade Path** — A deadly poppy field with stat checks and a guardian fight; rewards a level-up
   - **Forest Path** — Meet an adventurer who may join you as a companion (if you're strong or wealthy enough)
6. **Bandit Leader** — The final battle. Companions double your attack damage

### Combat System

Turn-based combat with four actions:
- **Attack** — Deal damage (enhanced by spell buffs and companion)
- **Defend** — Take half damage, skip enemy turn
- **Drink Potion** — Heal 20-25 HP from inventory
- **Cast Spell** — Class-specific abilities using spell slots

Defeated enemies have a chance to drop health potions or trigger bonus skeleton fights.

### Save System

The game offers save points between major encounters. Progress is stored in `savegame.json` and can be loaded from the main menu.

## Project Structure

```
├── main.py              # Entry point and game loop
├── states.py            # State machine: game states and transitions
├── transitions.py       # Campsite, path choice, glade/forest narrative logic
├── combat.py            # Combat system, boss fights, and encounter scripting
├── player.py            # Character class, creation, stats, leveling
├── enemies.py           # Enemy class with randomized stats
├── items.py             # Inventory system
├── spells.py            # Spell casting and spell menu display
├── signals.py           # Observer pattern (Signal class for events)
├── save_game.py         # JSON save/load system
├── utils.py             # Game over / restart logic
└── data/
    ├── player_stats.py  # Class definitions and stat tables
    ├── enemy_stats.py   # Enemy health/attack ranges
    ├── item_stats.py    # Starting inventory
    └── spell_stats.py   # Spell definitions per class
```

### Architecture Highlights

- **State machine** — Each game section is a `State` subclass with `enter`, `update`, and `exit` methods. The game loop drives transitions by calling `update()` which returns the next state (or `None` to end).
- **Signal system** — A lightweight observer pattern (`Signal` class) used for combat event notifications (damage taken, death).
- **Data/logic separation** — Game data (stats, spells, items) lives in `data/` modules, kept separate from the logic that uses it.
- **Serialization** — Characters serialize to/from dictionaries for JSON save files.

## Learning Context

This project is a hands-on learning vehicle for building foundational Python skills (OOP, control flow, data structures, multi-file architecture) that will transfer to GDScript for future game development in Godot.
