# Branching Paths Design

## Overview

Add branching narrative paths after the pixie encounter. Player chooses between two routes that offer different rewards, then converge for a final combat encounter with path-specific bonuses.

## Branch Point

After surviving the pixie encounter, player reaches a fork:

- **Option 1: "Continue to the clearing ahead"** → Glade Path
- **Option 2: "Turn back and take the forest trail"** → Forest Path

New state `PATH_CHOICE` comes after `PIXIE_ENCOUNTER`.

## Glade Path (Poppy Field Trap)

A beautiful meadow that's actually a trap - the poppies drug/drain the player.

### Challenge Layers

1. **Opening puzzle** - Choice about how to proceed (rush through, move carefully, look for another way). Wrong choice leads to harder stat check or combat.

2. **Stat check** - Player loses health pushing through the field. If health drops too low, they collapse and face combat.

3. **Potential combat** - If puzzle/stat check fails, an enemy awakens (new enemy like "Poppy Guardian"). If passed, combat is avoided.

### Reward

Level up: +10 max health, +3 attack

## Forest Path (Adventurer Encounter)

Player takes the longer route and finds another traveler resting by a fire.

### Encounter Flow

1. **Introduction** - Describe the adventurer (capable but weary)

2. **Dialogue choice:**
   - "Ask them to join you" → Triggers stat check
   - "Offer gold for their help" → Costs 10 gold, automatic success
   - "Leave them be" → Continue alone

3. **Stat check** (if persuading) - Based on current health or attack power
   - Pass → They join for free
   - Fail → They refuse, can still offer gold or leave

### Reward

Companion joins: `has_companion = True` on character

## Final Combat

New encounter after paths converge. New enemy (bandit, troll, or similar).

### Path Bonuses

- **Glade path:** Higher max_health and attack from level up
- **Forest path:** Damage doubled due to companion (`damage * 2`)

Both bonuses provide roughly equal power through different mechanics.

## Ending Variations

`VICTORY` state checks path taken and companion status:

- **Glade path:** "Battered but powerful, you emerge from the wilderness alone. The trials have made you stronger."
- **Forest path with companion:** "You and your new ally share a moment of triumph. The journey forged a bond between you."
- **Forest path alone:** "You make it through, though you wonder what might have been if you'd convinced that adventurer to join you."

## State Flow

```
PIXIE_ENCOUNTER
      |
  PATH_CHOICE
    /       \
GLADE_PATH  FOREST_PATH
    \       /
  FINAL_COMBAT
      |
   VICTORY (with variations)
```

## New Data Required

- New enemy: "Poppy Guardian" (for glade combat)
- New enemy: Final combat enemy (bandit/troll)
- Character attribute: `has_companion` (boolean)
- Character attribute or variable: `path_taken` (for ending text)

## Skills Practiced

- Branching state machines
- Stat checks and conditional logic
- Storing/checking player choices
- Multiple paths converging to shared state
