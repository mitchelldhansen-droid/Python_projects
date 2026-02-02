# Spell Slots System Implementation Plan

## Goal
Add a spell slots system with completely unique spells per class. Spell slots are limited casts that reset on rest.

## Overview

| Class | Base Slots | Bonus from Magic | Total | Spells |
|-------|------------|------------------|-------|--------|
| Warrior (magic 5) | 2 | +0 | 2 | Battle Cry, Second Wind |
| Rogue (magic 8) | 3 | +0 | 3 | Shadow Step, Poison Blade |
| Paladin (magic 12) | 4 | +1 | 5 | Lay on Hands, Smite |
| Mage (magic 20) | 5 | +2 | 7 | Fireball, Arcane Shield, Lightning Bolt |

Formula: `total_slots = BASE_SLOTS + (magic // 10)`

---

## Phase 1: Spell Data (data/spell_stats.py)

**Create new file** with spell definitions for each class.

Each spell has:
- `name`: Display name
- `description`: Short text
- `effect`: One of `damage`, `heal`, `buff_attack`, `shield`, `dodge_next`
- `power`: Base value for the effect
- `slots_required`: Cost to cast (1 or 2)

Also define `CLASS_SPELLS` (maps class name to spell dict) and `BASE_SPELL_SLOTS` (maps class to base slot count).

**Test:** Import the data in Python REPL, print spell values.

---

## Phase 2: Character Spell Tracking (player.py)

**Add to `Character.__init__`:**
- `self.max_spell_slots` - calculated from class + magic
- `self.current_spell_slots` - starts at max
- `self.active_buffs = {}` - tracks temporary combat effects

**Add methods:**
- `_calculate_max_slots()` - returns BASE + magic//10
- `get_available_spells()` - returns CLASS_SPELLS for this class
- `can_cast(spell_key)` - checks if enough slots
- `use_spell_slots(amount)` - decrements current slots
- `restore_spell_slots()` - resets to max (called on rest)

**Update `level_up()`:** Recalculate max slots after magic increases.

**Test:** Create characters of each class, check slot counts, test use/restore.

---

## Phase 3: Spell Casting Logic (spells.py)

**Create new file** with:

`display_spell_menu(character)`:
- Shows available spells with costs
- Marks which can/cannot be cast
- Returns spell list for selection

`cast_spell(character, spell_key, target=None)`:
- Validates spell exists and slots available
- Consumes slots
- Calculates power (base * magic multiplier)
- Applies effect based on type:
  - `damage`: target.take_damage()
  - `heal`: character.heal()
  - `buff_attack`: add to active_buffs (consumed on next attack)
  - `shield`: add to active_buffs (absorbs next incoming damage)
  - `dodge_next`: add to active_buffs (skip next enemy attack)
- Returns result dict with success, message, effect details

**Test:** Cast spells in REPL, verify effects apply correctly.

---

## Phase 4: Combat Integration (combat.py)

**Update combat menu:**
```
1. Attack
2. Defend
3. Drink Potion
4. Cast Spell
```

**Handle action "4":**
- Display spell menu
- Get player choice
- Call cast_spell()
- Handle success/failure

**Modify attack action:**
- Check for `attack_bonus` in active_buffs
- Add bonus to damage, remove buff

**Modify enemy attack phase:**
- Check for `dodge` buff - skip damage if present
- Check for `shield` buff - absorb damage up to shield value

**Update status display:** Show spell slots alongside health/potions.

**Test:** Run combat, cast spells, verify buffs work.

---

## Phase 5: Rest Integration (main.py)

**Update `rest()` function:**
- Call `character.restore_spell_slots()` after healing

**Test:** Rest at campsite, verify slots restore.

---

## Phase 6: Display Polish

**combat.py:** Add spell slots to combat status line.

**player.py:** Update `display()` to show spell slots cleanly.

---

## Files Summary

| File | Action |
|------|--------|
| `data/spell_stats.py` | CREATE - spell data |
| `spells.py` | CREATE - casting logic |
| `player.py` | MODIFY - add slot tracking |
| `combat.py` | MODIFY - add spell menu + buff handling |
| `main.py` | MODIFY - restore slots on rest |

---

## Git Workflow

```bash
git checkout -b feature/spell-slots

# Commit after each phase:
# Phase 1: "Add spell data for all classes"
# Phase 2: "Add spell slot tracking to Character class"
# Phase 3: "Add spell casting logic module"
# Phase 4: "Integrate spells into combat menu"
# Phase 5-6: "Add spell restoration and display updates"

git checkout main && git merge feature/spell-slots
```

---

## Verification

After each phase, test in Python REPL before moving on.

Final test: Play through the game as a Mage, cast spells in combat, rest at campsite, verify slots restore.

---

## Spell Reference

**Warrior:**
- Battle Cry (1 slot): +10 damage on next attack
- Second Wind (1 slot): Heal 15 HP

**Mage:**
- Fireball (1 slot): 25 damage
- Arcane Shield (1 slot): Absorb 20 damage
- Lightning Bolt (2 slots): 35 damage

**Rogue:**
- Shadow Step (1 slot): Dodge next attack
- Poison Blade (1 slot): +8 damage on next attack

**Paladin:**
- Lay on Hands (2 slots): Heal 30 HP
- Smite (1 slot): 20 damage
