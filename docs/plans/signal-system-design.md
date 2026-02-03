# Signal System Design

## Goal
Add an event/signal system to decouple game systems. This pattern is fundamental to Godot/GDScript and will transfer directly.

## What Signals Solve

**Before (tight coupling):**
- `combat.py` handles damage, printing, death checks, UI updates
- Adding features means modifying existing functions
- Everything knows about everything

**After (loose coupling):**
- `combat.py` handles combat logic only
- Other systems *listen* for events and react
- Adding features means connecting to existing signals

---

## The Signal Class

```python
class Signal:
    def __init__(self):
        self._listeners = []

    def connect(self, func):
        """Subscribe a function to this signal"""
        self._listeners.append(func)

    def disconnect(self, func):
        """Unsubscribe a function from this signal"""
        if func in self._listeners:
            self._listeners.remove(func)

    def emit(self, *args):
        """Notify all listeners with the given arguments"""
        for func in self._listeners:
            func(*args)
```

---

## Signals to Add

### Character Signals
| Signal | Emitted When | Arguments |
|--------|--------------|-----------|
| `damaged` | Takes damage | `(character, amount)` |
| `healed` | Heals HP | `(character, amount)` |
| `died` | Health reaches 0 | `(character,)` |
| `spell_cast` | Casts a spell | `(character, spell_name)` |
| `level_up` | Levels up | `(character, new_level)` |

### Enemy Signals
| Signal | Emitted When | Arguments |
|--------|--------------|-----------|
| `damaged` | Takes damage | `(enemy, amount)` |
| `died` | Health reaches 0 | `(enemy,)` |

---

## Implementation Phases

### Phase 1: Create Signal Class
- Create `signals.py` with the Signal class
- Test in REPL: create signal, connect print, emit

### Phase 2: Add Signals to Character
- Import Signal in `player.py`
- Add signal attributes in `__init__`
- Update `take_damage()` to emit `damaged` and `died`
- Update `heal()` to emit `healed`
- Test in REPL

### Phase 3: Add Signals to Enemy
- Import Signal in `enemies.py`
- Add signal attributes
- Update `take_damage()` to emit signals
- Test in REPL

### Phase 4: Refactor Combat Display
- Create simple listener functions for combat output
- Connect them at start of combat
- Remove hardcoded prints from damage/heal methods
- Verify game still works

---

## Files Summary

| File | Action |
|------|--------|
| `signals.py` | CREATE - Signal class |
| `player.py` | MODIFY - add signals to Character |
| `enemies.py` | MODIFY - add signals to Enemy |
| `combat.py` | MODIFY - connect listeners, remove some prints |

---

## Testing Strategy

After each phase, test in REPL:

```python
# Phase 1 test
from signals import Signal
s = Signal()
s.connect(print)
s.emit("Hello!")  # should print "Hello!"

# Phase 2 test
from player import Character
c = Character("Test", "Mage")
c.damaged.connect(lambda char, amt: print(f"SIGNAL: {char.name} took {amt}"))
c.take_damage(10)  # should trigger the signal
```

---

## Godot Equivalent

This Python pattern translates directly:

**Python (what we're building):**
```python
self.damaged = Signal()
self.damaged.connect(update_ui)
self.damaged.emit(self, 25)
```

**GDScript (what you'll write in Godot):**
```gdscript
signal damaged
damaged.connect(update_ui)
damaged.emit(self, 25)
```

Nearly identical syntax. The concept transfers 1:1.

---

## Git Workflow

```bash
git checkout -b feature/signals

# Commit after each phase:
# Phase 1: "Add Signal class"
# Phase 2: "Add signals to Character class"
# Phase 3: "Add signals to Enemy class"
# Phase 4: "Refactor combat to use signal listeners"

git checkout main && git merge feature/signals
```
